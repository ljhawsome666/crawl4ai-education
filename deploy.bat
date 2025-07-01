@echo off
echo === 创建虚拟环境 ===
python -m venv venv

echo === 激活虚拟环境 ===
call venv\Scripts\activate.bat

echo === 升级 pip 并安装依赖 ===
python -m pip install --upgrade pip
pip install -r backend\requirements.txt

echo === 安装 Playwright 并初始化浏览器 ===
python -m playwright install chromium

echo === 进行数据库迁移 ===
cd backend
python manage.py migrations
python manage.py migrate

echo.
echo ==== 部署完成！可运行开发服务器：====
echo.
echo     venv\Scripts\activate
echo     python manage.py runserver
pause

echo.
echo ==== 运行前端：====
echo.
echo    npm run dev