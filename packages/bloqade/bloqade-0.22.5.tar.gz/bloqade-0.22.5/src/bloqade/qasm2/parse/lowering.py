from dataclasses import dataclass

from kirin import ir, lowering
from kirin.dialects import cf, func, ilist
from kirin.lowering import LoweringState
from kirin.exceptions import DialectLoweringError
from bloqade.qasm2.types import CRegType, QRegType
from bloqade.qasm2.dialects import uop, core, expr, glob, noise, parallel

from . import ast
from .visitor import Visitor


@dataclass
class LoweringQASM(Visitor[lowering.Result]):
    state: LoweringState
    extension: str | None = None

    def visit_MainProgram(self, node: ast.MainProgram) -> lowering.Result:
        allowed = {dialect.name for dialect in self.state.dialects}
        if isinstance(node.header, ast.OPENQASM) and node.header.version.major == 2:
            dialects = ["qasm2.core", "qasm2.uop", "qasm2.expr"]
        elif isinstance(node.header, ast.Kirin):
            dialects = node.header.dialects

        for dialect in dialects:
            if dialect not in allowed:
                raise DialectLoweringError(
                    f"Dialect {dialect} not found, allowed: {', '.join(allowed)}"
                )

        for stmt in node.statements:
            self.visit(stmt)
        return lowering.Result()

    def visit_QReg(self, node: ast.QReg) -> lowering.Result:
        reg = core.QRegNew(
            self.state.append_stmt(expr.ConstInt(value=node.size)).result
        )
        self.state.append_stmt(reg)
        self.state.current_frame.defs[node.name] = reg.result
        return lowering.Result()

    def visit_CReg(self, node: ast.CReg) -> lowering.Result:
        reg = core.CRegNew(
            self.state.append_stmt(expr.ConstInt(value=node.size)).result
        )
        self.state.append_stmt(reg)
        self.state.current_frame.defs[node.name] = reg.result
        return lowering.Result()

    def visit_Barrier(self, node: ast.Barrier) -> lowering.Result:
        self.state.append_stmt(
            uop.Barrier(
                qargs=tuple(self.visit(qarg).expect_one() for qarg in node.qargs)
            )
        )
        return lowering.Result()

    def visit_CXGate(self, node: ast.CXGate) -> lowering.Result:
        self.state.append_stmt(
            uop.CX(
                ctrl=self.visit(node.ctrl).expect_one(),
                qarg=self.visit(node.qarg).expect_one(),
            )
        )
        return lowering.Result()

    def visit_Measure(self, node: ast.Measure) -> lowering.Result:
        self.state.append_stmt(
            core.Measure(
                qarg=self.visit(node.qarg).expect_one(),
                carg=self.visit(node.carg).expect_one(),
            )
        )
        return lowering.Result()

    def visit_UGate(self, node: ast.UGate) -> lowering.Result:
        self.state.append_stmt(
            uop.UGate(
                theta=self.visit(node.theta).expect_one(),
                phi=self.visit(node.phi).expect_one(),
                lam=self.visit(node.lam).expect_one(),
                qarg=self.visit(node.qarg).expect_one(),
            )
        )
        return lowering.Result()

    def visit_Reset(self, node: ast.Reset) -> lowering.Result:
        self.state.append_stmt(core.Reset(qarg=self.visit(node.qarg).expect_one()))
        return lowering.Result()

    def visit_IfStmt(self, node: ast.IfStmt) -> lowering.Result:
        cond_stmt = core.CRegEq(
            lhs=self.visit(node.cond.lhs).expect_one(),
            rhs=self.visit(node.cond.rhs).expect_one(),
        )
        cond = self.state.append_stmt(cond_stmt).result
        frame = self.state.current_frame
        before_block = frame.curr_block
        if frame.exit_block is None:
            raise DialectLoweringError("code block is not exiting")
        else:
            before_block_next = frame.exit_block
        if_block = self.state.current_frame.append_block()
        for stmt in node.body:
            self.visit(stmt)

        if_block.stmts.append(
            cf.Branch(
                arguments=(),
                successor=before_block_next,
            )
        )
        before_block.stmts.append(
            cf.ConditionalBranch(
                cond=cond,
                then_arguments=(),
                then_successor=if_block,
                else_arguments=(),
                else_successor=before_block_next,
            )
        )
        frame.curr_block = before_block_next
        return lowering.Result()

    def visit_BinOp(self, node: ast.BinOp) -> lowering.Result:
        if node.op == "+":
            stmt_type = expr.Add
        elif node.op == "-":
            stmt_type = expr.Sub
        elif node.op == "*":
            stmt_type = expr.Mul
        else:
            stmt_type = expr.Div

        stmt = self.state.append_stmt(
            stmt_type(
                lhs=self.visit(node.lhs).expect_one(),
                rhs=self.visit(node.rhs).expect_one(),
            )
        )
        return lowering.Result(stmt.result)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> lowering.Result:
        if node.op == "-":
            stmt = expr.Neg(value=self.visit(node.operand).expect_one())
            return lowering.Result(stmt.result)
        else:
            return lowering.Result(self.visit(node.operand).expect_one())

    def visit_Bit(self, node: ast.Bit) -> lowering.Result:
        if node.name.id not in self.state.current_frame.defs:
            raise ValueError(f"Bit {node.name} not found")

        addr = self.state.append_stmt(expr.ConstInt(value=node.addr))
        reg = self.state.current_frame.get_local(node.name.id)
        if reg is None:
            raise DialectLoweringError(f"{node.name.id} is not defined")

        if reg.type.is_subseteq(QRegType):
            stmt = core.QRegGet(reg, addr.result)
        elif reg.type.is_subseteq(CRegType):
            stmt = core.CRegGet(reg, addr.result)
        return lowering.Result(self.state.append_stmt(stmt).result)

    def visit_Call(self, node: ast.Call) -> lowering.Result:
        if node.name == "cos":
            stmt = expr.Cos(self.visit(node.args[0]).expect_one())
        elif node.name == "sin":
            stmt = expr.Sin(self.visit(node.args[0]).expect_one())
        elif node.name == "tan":
            stmt = expr.Tan(self.visit(node.args[0]).expect_one())
        elif node.name == "exp":
            stmt = expr.Exp(self.visit(node.args[0]).expect_one())
        elif node.name == "log":
            stmt = expr.Log(self.visit(node.args[0]).expect_one())
        elif node.name == "sqrt":
            stmt = expr.Sqrt(self.visit(node.args[0]).expect_one())
        else:
            raise ValueError(f"Unknown function {node.name}")
        self.state.append_stmt(stmt)
        return lowering.Result(stmt.result)

    def visit_Instruction(self, node: ast.Instruction) -> lowering.Result:
        params = [self.visit(param).expect_one() for param in node.params]
        qargs = [self.visit(qarg).expect_one() for qarg in node.qargs]
        visit_inst = getattr(self, "visit_instruction_" + node.name.id, None)
        if visit_inst is not None:
            self.state.append_stmt(visit_inst(node, params, qargs))
        else:
            value = self.state.get_global(node.name.id).expect(ir.Method)
            # NOTE: QASM expects the return type to be known at call site
            if value.return_type is None:
                raise ValueError(f"Unknown return type for {node.name.id}")
            self.state.append_stmt(
                func.Invoke(
                    callee=value,
                    inputs=tuple(params + qargs),
                    kwargs=tuple(),
                )
            )
        return lowering.Result()

    def visit_instruction_id(self, node: ast.Instruction, params, qargs):
        return uop.Id(qarg=qargs[0])

    def visit_instruction_x(self, node: ast.Instruction, params, qargs):
        return uop.X(qarg=qargs[0])

    def visit_instruction_y(self, node: ast.Instruction, params, qargs):
        return uop.Y(qarg=qargs[0])

    def visit_instruction_z(self, node: ast.Instruction, params, qargs):
        return uop.Z(qarg=qargs[0])

    def visit_instruction_h(self, node: ast.Instruction, params, qargs):
        return uop.H(qarg=qargs[0])

    def visit_instruction_s(self, node: ast.Instruction, params, qargs):
        return uop.S(qarg=qargs[0])

    def visit_instruction_sdg(self, node: ast.Instruction, params, qargs):
        return uop.Sdag(qarg=qargs[0])

    def visit_instruction_sx(self, node: ast.Instruction, params, qargs):
        return uop.SX(qarg=qargs[0])

    def visit_instruction_sxdg(self, node: ast.Instruction, params, qargs):
        return uop.SXdag(qarg=qargs[0])

    def visit_instruction_t(self, node: ast.Instruction, params, qargs):
        return uop.T(qarg=qargs[0])

    def visit_instruction_tdg(self, node: ast.Instruction, params, qargs):
        return uop.Tdag(qarg=qargs[0])

    def visit_instruction_rx(self, node: ast.Instruction, params, qargs):
        return uop.RX(theta=params[0], qarg=qargs[0])

    def visit_instruction_ry(self, node: ast.Instruction, params, qargs):
        return uop.RY(theta=params[0], qarg=qargs[0])

    def visit_instruction_rz(self, node: ast.Instruction, params, qargs):
        return uop.RZ(theta=params[0], qarg=qargs[0])

    def visit_instruction_p(self, node: ast.Instruction, params, qargs):
        return uop.U1(lam=params[0], qarg=qargs[0])

    def visit_instruction_u(self, node: ast.Instruction, params, qargs):
        return uop.UGate(theta=params[0], phi=params[1], lam=params[2], qarg=qargs[0])

    def visit_instruction_u1(self, node: ast.Instruction, params, qargs):
        return uop.U1(lam=params[0], qarg=qargs[0])

    def visit_instruction_u2(self, node: ast.Instruction, params, qargs):
        return uop.U2(phi=params[0], lam=params[1], qarg=qargs[0])

    def visit_instruction_u3(self, node: ast.Instruction, params, qargs):
        return uop.UGate(theta=params[0], phi=params[1], lam=params[2], qarg=qargs[0])

    def visit_instruction_CX(self, node: ast.Instruction, params, qargs):
        return uop.CX(ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_cx(self, node: ast.Instruction, params, qargs):
        return uop.CX(ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_cy(self, node: ast.Instruction, params, qargs):
        return uop.CY(ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_cz(self, node: ast.Instruction, params, qargs):
        return uop.CZ(ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_ch(self, node: ast.Instruction, params, qargs):
        return uop.CH(ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_crx(self, node: ast.Instruction, params, qargs):
        return uop.CRX(lam=params[0], ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_cry(self, node: ast.Instruction, params, qargs):
        return uop.CRY(lam=params[0], ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_crz(self, node: ast.Instruction, params, qargs):
        return uop.CRZ(lam=params[0], ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_ccx(self, node: ast.Instruction, params, qargs):
        return uop.CCX(ctrl1=qargs[0], ctrl2=qargs[1], qarg=qargs[2])

    def visit_instruction_csx(self, node: ast.Instruction, params, qargs):
        return uop.CSX(ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_cswap(self, node: ast.Instruction, params, qargs):
        return uop.CSwap(ctrl=qargs[0], qarg1=qargs[1], qarg2=qargs[2])

    def visit_instruction_cp(self, node: ast.Instruction, params, qargs):
        return uop.CU1(lam=params[0], ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_cu1(self, node: ast.Instruction, params, qargs):
        return uop.CU1(lam=params[0], ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_cu3(self, node: ast.Instruction, params, qargs):
        return uop.CU3(
            theta=params[0], phi=params[1], lam=params[2], ctrl=qargs[0], qarg=qargs[1]
        )

    def visit_instruction_cu(self, node: ast.Instruction, params, qargs):
        return uop.CU3(
            theta=params[0], phi=params[1], lam=params[2], ctrl=qargs[0], qarg=qargs[1]
        )

    def visit_instruction_rxx(self, node: ast.Instruction, params, qargs):
        return uop.RXX(theta=params[0], ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_rzz(self, node: ast.Instruction, params, qargs):
        return uop.RZZ(theta=params[0], ctrl=qargs[0], qarg=qargs[1])

    def visit_instruction_swap(self, node: ast.Instruction, params, qargs):
        return uop.Swap(ctrl=qargs[0], qarg=qargs[1])

    def visit_Number(self, node: ast.Number) -> lowering.Result:
        if isinstance(node.value, int):
            stmt = expr.ConstInt(value=node.value)
        else:
            stmt = expr.ConstFloat(value=node.value)
        return lowering.Result(self.state.append_stmt(stmt).result)

    def visit_Pi(self, node: ast.Pi) -> lowering.Result:
        return lowering.Result(self.state.append_stmt(expr.ConstPI()).result)

    def visit_Include(self, node: ast.Include) -> lowering.Result:
        if node.filename not in ["qelib1.inc"]:
            raise DialectLoweringError(f"Include {node.filename} not found")

        return lowering.Result()

    def visit_Gate(self, node: ast.Gate) -> lowering.Result:
        raise NotImplementedError("Gate lowering not supported")

    def visit_Name(self, node: ast.Name) -> lowering.Result:
        if (value := self.state.current_frame.get_local(node.id)) is not None:
            return lowering.Result(value)
        raise ValueError(f"name {node.id} not found")

    def visit_ParaCZGate(self, node: ast.ParaCZGate) -> lowering.Result:
        ctrls: list[ir.SSAValue] = []
        qargs: list[ir.SSAValue] = []
        for pair in node.qargs:
            if len(pair) != 2:
                raise ValueError("CZ gate requires exactly two qargs")
            ctrl, qarg = pair
            ctrls.append(self.visit(ctrl).expect_one())
            qargs.append(self.visit(qarg).expect_one())

        ctrls_stmt = ilist.New(values=ctrls)
        qargs_stmt = ilist.New(values=qargs)
        self.state.append_stmt(ctrls_stmt)
        self.state.append_stmt(qargs_stmt)
        self.state.append_stmt(
            parallel.CZ(ctrls=ctrls_stmt.result, qargs=qargs_stmt.result)
        )
        return lowering.Result()

    def visit_ParaRZGate(self, node: ast.ParaRZGate) -> lowering.Result:
        qargs: list[ir.SSAValue] = []
        for pair in node.qargs:
            if len(pair) != 1:
                raise ValueError("Rz gate requires exactly one qarg")
            qargs.append(self.visit(pair[0]).expect_one())

        qargs_stmt = ilist.New(values=qargs)
        self.state.append_stmt(qargs_stmt)
        self.state.append_stmt(
            parallel.RZ(
                theta=self.visit(node.theta).expect_one(),
                qargs=qargs_stmt.result,
            )
        )
        return lowering.Result()

    def visit_ParaU3Gate(self, node: ast.ParaU3Gate) -> lowering.Result:
        qargs: list[ir.SSAValue] = []
        for pair in node.qargs:
            if len(pair) != 1:
                raise ValueError("U3 gate requires exactly one qarg")
            qargs.append(self.visit(pair[0]).expect_one())

        qargs_stmt = ilist.New(values=qargs)
        self.state.append_stmt(qargs_stmt)
        self.state.append_stmt(
            parallel.UGate(
                theta=self.visit(node.theta).expect_one(),
                phi=self.visit(node.phi).expect_one(),
                lam=self.visit(node.lam).expect_one(),
                qargs=qargs_stmt.result,
            )
        )
        return lowering.Result()

    def visit_GlobUGate(self, node: ast.GlobUGate) -> lowering.Result:

        registers: list[ir.SSAValue] = []

        for register in node.registers:  # These will all be ast.Names
            registers.append(self.visit(register).expect_one())

        registers_stmt = ilist.New(values=registers)
        self.state.append_stmt(registers_stmt)
        self.state.append_stmt(
            # all the stuff going into the args should be SSA values
            glob.UGate(
                registers=registers_stmt.result,  # expect_one = a singular SSA value
                theta=self.visit(node.theta).expect_one(),
                phi=self.visit(node.phi).expect_one(),
                lam=self.visit(node.lam).expect_one(),
            )
        )
        return lowering.Result()

    def visit_NoisePAULI1(self, node: ast.NoisePAULI1) -> lowering.Result:
        self.state.append_stmt(
            noise.Pauli1(
                px=self.visit(node.px).expect_one(),
                py=self.visit(node.py).expect_one(),
                pz=self.visit(node.pz).expect_one(),
                qarg=self.visit(node.qarg).expect_one(),
            )
        )
        return lowering.Result()
