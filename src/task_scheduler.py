import csv
import tempfile
import subprocess

from dataclasses import dataclass


@dataclass
class TaskSchedulerAttribution:
    """
    タスクの属性情報のデータクラス
    変数のコメントは、コマンドの出力結果のヘッダ名を参照したもの
    """
    host_name: str # ホスト名
    task_name: str # タスク名
    next_run_time: str # 次回の実行時刻
    status: str # 状態
    logon_mode: str # ログオン モード
    last_run_time: str # 前回の実行時刻
    last_result: str # 前回の結果
    author: str # 作成者
    task_to_run: str # 実行するタスク
    start_in: str # 開始
    comment: str # コメント
    scheduled_task_state: str # スケジュールされたタスクの状態
    idle_time: str # アイドル時間
    power_management: str # 電源管理
    run_as_user: str # ユーザーとして実行
    delete_task_rescheduled_case: str # 再度スケジュールされない場合はタスクを削除する
    task_stopping_up_to_time: str # タスクを停止するまでの時間
    schedule: str # スケジュール
    schedule_type: str # スケジュールの種類
    start_time: str # 開始時刻
    start_date: str # 開始日
    end_date: str # 終了日
    days: str # 日
    months: str # 月
    repeat_interval: str # 繰り返し: 間隔
    repeat_end_time: str # 繰り返し: 終了時刻
    repeat_duration: str # 繰り返し: 期間
    repeat_stop_if_idle: str # 繰り返し: 実行中の場合は停止


class TaskSchedulerOperation:

    def __init__(self):
        self.task_names = self.get_task_names()


    def get_task_names(self) -> set:
        """タスク名を取得

        Returns:
            set: タスク名の集合データ
        """
        command = ['schtasks', '/Query', '/NH', '/FO', 'CSV']
        _output = subprocess.check_output(command)
        output = _output.decode('cp932').replace('\r', '')

        task_names = []
        with tempfile.TemporaryFile(mode="w+") as f:
            f.write(output)
            f.seek(0)
            reader = csv.reader(f)
            for r in reader:
                if r[0] != '':
                    task_names.append(r[0])
                else:
                    continue
        return set(task_names)


    def get_task_attributuion(self, task_name: str) -> TaskSchedulerAttribution:
        """タスクの属性情報を取得

        Args:
            task_name (str): タスク名

        Returns:
            TaskAttribution: タスクの属性情報
        """
        command = ['schtasks', '/Query', '/NH', '/TN', task_name, '/V', '/FO', 'CSV']
        _output = subprocess.check_output(command)
        output = _output.decode('cp932').replace('\r', '')

        with tempfile.TemporaryFile(mode="w+") as f:
            f.write(output)
            f.seek(0)
            reader = csv.reader(f)

            for r in reader:
                task_attribution = TaskSchedulerAttribution(*r)
        return task_attribution


    def run_task(self, task_name: str) -> subprocess.CompletedProcess:
        """タスクを実行

        Args:
            task_name (str): タスク名
        """
        command = ['schtasks', '/Run', '/TN', task_name]
        return subprocess.run(command, capture_output=True, text=True)


    def stop_task(self, task_name: str) -> subprocess.CompletedProcess:
        """タスクを停止

        Args:
            task_name (str): タスク名
        """
        command = ['schtasks', '/End', '/TN', task_name]
        return subprocess.run(command, capture_output=True, text=True)



    def delete_task(self, task_name: str) -> subprocess.CompletedProcess:
        """タスクを削除

        Args:
            task_name (str): タスク名
        """
        command = ['schtasks', '/Delete', '/TN', task_name, '/F']
        return subprocess.run(command, capture_output=True, text=True)


    def create_task(
        self,
        task_name: str,
        task_to_run: str,
        schedule: str
    ) -> subprocess.CompletedProcess:
        """タスクを作成

        Args:
            task_name (str): タスク名
            task_to_run (str): 実行するタスク
            schedule (str): スケジュール
        """
        command = [
            'schtasks',
            '/Create',
            '/TN', task_name,
            '/TR', task_to_run,
            '/SC', schedule
        ]
        return subprocess.run(command, capture_output=True, text=True)


    def change_task(
        self,
        task_name: str,
        task_to_run: str,
        schedule: str
    ) -> subprocess.CompletedProcess:
        """タスクを変更

        Args:
            task_name (str): タスク名
            task_to_run (str): 実行するタスク
            schedule (str): スケジュール
        """
        command = [
            'schtasks',
            '/Change',
            '/TN', task_name,
            '/TR', task_to_run,
            '/SC', schedule
        ]
        return subprocess.run(command, capture_output=True, text=True)


    def enable_task(self, task_name: str) -> subprocess.CompletedProcess:
        """タスクを有効化

        Args:
            task_name (str): タスク名
        """
        command = ['schtasks', '/Change', '/TN', task_name, '/ENABLE']
        return subprocess.run(command, capture_output=True, text=True)


    def disable_task(self, task_name: str) -> subprocess.CompletedProcess:
        """タスクを無効化

        Args:
            task_name (str): タスク名
        """
        command = ['schtasks', '/Change', '/TN', task_name, '/DISABLE']
        return subprocess.run(command, capture_output=True, text=True)
