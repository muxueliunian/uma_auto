import run_as_admin
import image_recogniton
import jjc
import sys
from PyQt6.QtWidgets import QApplication,QDialog,QPushButton,QHBoxLayout,QMessageBox

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.resize(200, 180)
        
        # 创建布局和按钮
        hbox = QHBoxLayout()
        self.button = QPushButton("自动打JJC", self)
        
        # 绑定点击事件
        self.button.clicked.connect(self.on_jjc_button_click)
        
        hbox.addWidget(self.button)
        self.setLayout(hbox)

    def on_jjc_button_click(self):
        """按钮点击事件处理函数"""
        # 添加确认对话框
        reply = QMessageBox.question(
            self,
            '确认操作',
            '确定要开始自动打JJC吗？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # 调用实际功能函数
                jjc.fuck_jjc()  # 你的实际功能函数
                QMessageBox.information(
                    self, 
                    '完成', 
                    'JJC自动战斗已执行！'
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    '错误',
                    f'执行出错: {str(e)}'
                )

#主函数
def main():
    # run_as_admin.is_admin()
    # jjc.fuck_jjc()
    app = QApplication(sys.argv)
    window = MyDialog()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
