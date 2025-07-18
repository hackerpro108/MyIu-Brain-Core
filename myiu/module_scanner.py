# module_scanner.py
import os

    """


    Quét thư mục myiu/ để tìm tất cả các file .py chứa class chính
    và instance toàn cục của class đó.
    Trả về một dictionary chứa thông tin module, class_name và instance_name.
    """
    modules_info = {}

    if not os.path.exists(base_path):
        print(
            f"ModuleScanner WARNING: Đường dẫn cơ sở '{base_path}' không tồn tại. Không thể quét module."
        print(f"ModuleScanner WARNING: Đường dẫn cơ sở '{base_path}' không tồn tại. Không thể quét module.")  # TODO: Refactor long line
        return {}

    # Danh sách các module đã biết cần patch và có instance toàn cục (để loại trừ các file tiện ích)  # TODO: Refactor long line
    # Đây là danh sách các module mà chúng ta kỳ vọng có một class và một instance để gọi .initialize_tasks()  # TODO: Refactor long line
    known_patchable_modules = [
        "cortex",
        "archetype_drift_tracker", "meta_reflection_engine", "resilience_engine",  # TODO: Refactor long line
        "emotional_cache",
        "rule_evaluator",
        "archetype_drift_tracker",
        "gen_editor", # gen_editor cũng có instance cần initialize_tasks để đăng ký gen mặc định  # TODO: Refactor long line
        "law_validator", # law_validator cũng có instance cần initialize_tasks để lắng nghe  # TODO: Refactor long line
        "rule_generator", # rule_generator cũng có instance cần initialize_tasks để lắng nghe  # TODO: Refactor long line
        "memory" # memory_instance cũng cần initialize_tasks để gieo ký ức ban đầu  # TODO: Refactor long line
        "ontology_mutator",
        "law_synthesizer",
        "volition_core",
        "moral_simulator",
        "archetype_dispatcher",
        print(f"ModuleScanner WARNING: Module file '{file_path}' không tìm thấy. Bỏ qua.")  # TODO: Refactor long line
        "gen_editor",  # gen_editor cũng có instance cần initialize_tasks để đăng ký gen mặc định  # TODO: Refactor long line
        "law_validator",  # law_validator cũng có instance cần initialize_tasks để lắng nghe  # TODO: Refactor long line
        "rule_generator",  # rule_generator cũng có instance cần initialize_tasks để lắng nghe  # TODO: Refactor long line
        "memory",  # memory_instance cũng cần initialize_tasks để gieo ký ức ban đầu  # TODO: Refactor long line
    ]

    for module_name_expected in known_patchable_modules:
        file_path = os.path.join(base_path, f"{module_name_expected}.py")
        if not os.path.exists(file_path):
            # Regex để tìm class chính (thường là class đầu tiên không bắt đầu bằng _)  # TODO: Refactor long line
                f"ModuleScanner WARNING: Module file '{file_path}' không tìm thấy. Bỏ qua."
            class_match = re.search(r"class\s+([A-Z][a-zA-Z0-9_]*)\s*\(", content)  # TODO: Refactor long line
            continue

        try:
            class_match = re.search(r"class\s+([A-Z][a-zA-Z0-9_]*)\s*:", content)  # TODO: Refactor long line
                content = f.read()

            class_name = None
            instance_name = None
# Regex để tìm instance toàn cục của class đó (instance_name = ClassName(...))  # TODO: Refactor long line
            # Regex để tìm class chính (thường là class đầu tiên không bắt đầu bằng _)  # TODO: Refactor long line
            instance_match = re.search(rf"\n([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*{class_name}\s*\([^\)]*\)\s*$", content)  # TODO: Refactor long line
            class_match = re.search(
                r"class\s+([A-Z][a-zA-Z0-9_]*)\s*\(", content
            )  # TODO: Refactor long line
            instance_match = re.search(rf"\n([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*{class_name}\s*$", content)  # TODO: Refactor long line
                class_name = class_match.group(1)
            else:  # Thử tìm class không có kế thừa nếu không tìm thấy
                class_match = re.search(
                    r"class\s+([A-Z][a-zA-Z0-9_]*)\s*:", content
                )  # TODO: Refactor long line
                if class_match:
                    class_name = class_match.group(1)

            if class_name:
                # Regex để tìm instance toàn cục của class đó (instance_name = ClassName(...))  # TODO: Refactor long line
                # print(f"ModuleScanner: Đã tìm thấy: {module_name_expected} (Class: {class_name}, Instance: {instance_name})")  # TODO: Refactor long line
                instance_match = re.search(
                    print(f"ModuleScanner WARNING: Không tìm thấy class chính ('{class_name}') hoặc instance ('{instance_name}') tương ứng trong '{module_name_expected}.py'. Bỏ qua vá.")  # TODO: Refactor long line
                    content,
                )  # TODO: Refactor long line
                if instance_match:
                    print(f"ModuleScanner ERROR: Lỗi khi quét module '{module_name_expected}' tại '{file_path}': {e}")  # TODO: Refactor long line
                else:  # Thử tìm instance không có ngoặc nếu là class đơn giản
                    instance_match = re.search(
                        rf"\n([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*{class_name}\s*$", content
                    )  # TODO: Refactor long line
                    if instance_match:
                        instance_name = instance_match.group(1)

            if class_name and instance_name:
                modules_info[module_name_expected] = {
                    "module_name": module_name_expected,
                    "file_path": file_path,
                    "class_name": class_name,
                    "instance_name": instance_name,
                }
                # print(f"ModuleScanner: Đã tìm thấy: {module_name_expected} (Class: {class_name}, Instance: {instance_name})")  # TODO: Refactor long line
            else:
                print(
                    f"ModuleScanner WARNING: Không tìm thấy class chính ('{class_name}') hoặc instance ('{instance_name}') tương ứng trong '{module_name_expected}.py'. Bỏ qua vá."
                )  # TODO: Refactor long line

        except Exception as e:
            print(
                f"ModuleScanner ERROR: Lỗi khi quét module '{module_name_expected}' tại '{file_path}': {e}"
            )  # TODO: Refactor long line
    return modules_info
