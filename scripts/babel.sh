if [ $(pwd) == *scripts ]
then
    cd ../
fi
pybabel extract -F transparentai_ui/babel.cfg -o transparentai_ui/messages.pot .
# pybabel init -i transparentai_ui/messages.pot -d transparentai_ui/app/translations -l fr
pybabel update -i transparentai_ui/messages.pot -d transparentai_ui/app/translations
pybabel compile -d transparentai_ui/app/translations