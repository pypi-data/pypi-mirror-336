import os

from huggingface_hub import HfApi, HfFolder, Repository


def latest_model_path():
    directories = os.listdir("models")
    return f"models/{max(directories)}"


def is_git_repo(directory):
    return os.path.exists(os.path.join(directory, ".git"))


class HuggingFace:
    def __init__(self, repo_name="MatveyMerzlikin/ege-classification"):
        self.repo_name = repo_name
        self.token = HfFolder.get_token()
        self.api = HfApi(token=self.token)

    def save(self, model_path=None, commit_message="Обновление модели"):
        if not model_path:
            model_path = latest_model_path()

        print(f"Отправка модели из {model_path} в репозиторий {self.repo_name}...")

        try:
            self.api.upload_folder(
                folder_path=model_path,
                repo_id=self.repo_name,
                commit_message=commit_message,
                ignore_patterns=["**/.git*", "**/logs*", "**/*.tmp"],
            )
            print("Модель успешно отправлена в Hugging Face!")
        except Exception as e:
            print(f"Ошибка при отправке модели: {str(e)}")
            print("Проверьте правильность токена Hugging Face.")
