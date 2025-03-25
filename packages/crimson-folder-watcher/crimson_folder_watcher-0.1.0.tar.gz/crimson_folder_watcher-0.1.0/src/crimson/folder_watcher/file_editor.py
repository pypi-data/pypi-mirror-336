from typing import Callable, Dict, Tuple, Union
import os

# 수정된 타입 정의: (content, 선택적 대상 경로) 튜플을 반환
FileEditorFunc = Callable[[str, str], Union[str, Tuple[str, str]]]


class FileEditor:
    """
    Handles file editing operations when files are modified.
    """

    def __init__(self):
        """Initialize the file editor with an empty registry of edit functions."""
        self.edit_functions: Dict[str, FileEditorFunc] = {}

    def register(self, pattern: str, edit_func: FileEditorFunc) -> None:
        """
        Register an edit function for files matching a specific pattern.

        Args:
            pattern: File pattern to match (uses fnmatch syntax)
            edit_func: Function that accepts (src_path, content) and returns either:
                       - modified content (str)
                       - tuple of (modified content, new destination path)
        """
        self.edit_functions[pattern] = edit_func

    def edit_file(
        self, src_path: str, source_dir: str, output_dir: str
    ) -> Tuple[bool, str]:
        """
        Apply registered edit functions to a file.

        Args:
            src_path: Source file path
            dest_path: Original destination file path
            base_output_dir: Base output directory

        Returns:
            Tuple of (success, final_destination_path)
            - success: True if the file was edited and written
            - final_destination_path: The actual path where the file was written
        """
        import fnmatch

        ori_src_path = src_path.replace(source_dir, "")

        # 소스 파일의 기본 이름만 추출
        filename = os.path.basename(ori_src_path)

        # 패턴 매칭 함수 찾기
        matching_functions = [
            func
            for pattern, func in self.edit_functions.items()
            if fnmatch.fnmatch(filename, pattern)
        ]

        if not matching_functions:
            return False, src_path

        try:

            final_dest_path = None

            with open(src_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 매칭된 모든 편집 함수 적용
            for edit_func in matching_functions:
                result = edit_func(ori_src_path, content)

                # 함수가 튜플을 반환하면 내용과 새 경로를 모두 업데이트
                if isinstance(result, tuple) and len(result) == 2:
                    content, new_rel_path = result
                    if new_rel_path:  # 빈 문자열이 아니면 경로 업데이트
                        # 새 상대 경로를 기준으로 최종 경로 생성
                        final_dest_path = output_dir + new_rel_path
                else:
                    # 문자열만 반환한 경우 (내용만 업데이트)
                    content = result

            if final_dest_path is None:
                final_dest_path = output_dir + ori_src_path

            # 최종 경로의 디렉토리 존재 확인
            os.makedirs(os.path.dirname(final_dest_path), exist_ok=True)

            # 수정된 내용을 최종 경로에 쓰기
            with open(final_dest_path, "w", encoding="utf-8") as f:
                f.write(content)

            return True, final_dest_path
        except Exception as e:
            print(f"Error editing file {src_path}: {e}")
            return False, src_path
