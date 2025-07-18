# myiu/code_mutator.py
import ast
import astor  # Thư viện để chuyển đổi AST ngược lại thành code
import os
import shutil

from myiu.base_module import AsyncModule

from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from myiu.event_bus import EventBus


class CodeMutator(AsyncModule):
    """
    Nhà điêu khắc Mã nguồn. Thực thi các 'gen kiến trúc' để
    tự động tái cấu trúc (refactor) mã nguồn của chính MyIu.
    """

    def __init__(self, event_bus: "EventBus"):
        super().__init__()
        self.is_background_service = True
        self.event_bus = event_bus
        print("CodeMutator: Initialized. Ready to sculpt the source code.")

    async def _setup_async_tasks(self):
        """Lắng nghe các lệnh thực thi gen kiến trúc."""
        self.add_task(self._subscribe_to_architectural_genes())

    async def _subscribe_to_architectural_genes(self):
        """Lắng nghe các quyết định từ Hội đồng về việc thay đổi code."""
        # Giả định Hội đồng sẽ publish lên topic này
        request_queue = await self.event_bus.subscribe(
            "ARCHITECTURAL_GENE_EXECUTION"
        )  # TODO: Refactor long line
        while self._running:
            gene_data = await request_queue.get()
            await self._execute_architectural_gene(gene_data)

    async def _execute_architectural_gene(self, gene_data: Dict[str, Any]):
        """Thực thi một gen kiến trúc, ví dụ: refactor một hàm."""
        target_file = gene_data.get("target_file")
        action = gene_data.get("action")
        params = gene_data.get("params", {})

        if not all([target_file, action]):
            print(
                f"CodeMutator: Invalid architectural gene received: {gene_data}"  # TODO: Refactor long line
            )  # TODO: Refactor long line
            return

        if not os.path.exists(target_file):
            print(f"CodeMutator: Target file not found: {target_file}")
            return

        # Tạo backup trước khi sửa đổi
        backup_path = f"{target_file}.bak"
        shutil.copy(target_file, backup_path)
        print(f"CodeMutator: Created backup at '{backup_path}'.")

        try:
            with open(target_file, "r", encoding="utf-8") as f:
                source_code = f.read()

            # Phân tích mã nguồn thành cây cú pháp trừu tượng (AST)
            tree = ast.parse(source_code)

            # Thực hiện hành động sửa đổi trên cây AST
            if action == "rename_function":
                transformer = RenameFunctionTransformer(
                    params.get("old_name"), params.get("new_name")
                )  # TODO: Refactor long line
                new_tree = transformer.visit(tree)
                ast.fix_missing_locations(new_tree)

                # Chuyển cây AST đã sửa đổi ngược lại thành mã nguồn
                new_source_code = astor.to_source(new_tree)

                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(new_source_code)

                print(
                    f"CodeMutator: Successfully '{action}' on '{target_file}'."
                )  # TODO: Refactor long line
                # Thông báo cho hệ thống kiểm soát chất lượng
                await self.event_bus.publish(
                    "CODE_MUTATION_COMPLETED",
                    {"file_path": target_file, "backup_path": backup_path},
                )
        except Exception as e:
            print(
                f"CodeMutator: Failed to modify '{target_file}': {e}. Restoring from backup."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            # Nếu có lỗi, phục hồi từ backup
            shutil.move(backup_path, target_file)


class RenameFunctionTransformer(ast.NodeTransformer):
    """Một ví dụ về NodeTransformer để đổi tên một hàm trong cây AST."""

    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name

    def visit_FunctionDef(self, node):
        if node.name == self.old_name:
            print(
                f"AST Transformer: Renaming function '{node.name}' to '{self.new_name}'."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            node.name = self.new_name
        return self.generic_visit(node)
