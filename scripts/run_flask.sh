if [ $(pwd) == *scripts ]
then
    cd ../transparentai_ui/
else
    cd ./transparentai_ui/
fi
export FLASK_ENV=development
export FLASK_APP=run.py
flask run