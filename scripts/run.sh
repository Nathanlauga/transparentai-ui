if [ $(pwd) == *scripts ]
then
    cd ../transparentai-ui/
else
    cd ./transparentai-ui/
fi
gunicorn app:app