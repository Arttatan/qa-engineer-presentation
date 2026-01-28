# Инструкция по отправке на GitHub

## Шаг 1: Настройка Git (если еще не настроено)

Выполните в терминале следующие команды (замените на свои данные):

```bash
git config --global user.name "Ваше Имя"
git config --global user.email "ваш.email@example.com"
```

Или только для этого репозитория (без --global):

```bash
git config user.name "Ваше Имя"
git config user.email "ваш.email@example.com"
```

## Шаг 2: Создание коммита

После настройки git выполните:

```bash
cd c:\Users\35191\Presentation
git commit -m "Initial commit: QA Engineer presentation website"
```

## Шаг 3: Создание репозитория на GitHub

1. Перейдите на [GitHub.com](https://github.com)
2. Войдите в свой аккаунт (или создайте новый)
3. Нажмите кнопку **"+"** в правом верхнем углу → **"New repository"**
4. Заполните:
   - **Repository name**: `qa-engineer-presentation` (или любое другое имя)
   - **Description**: "Современный одностраничный сайт-презентация QA Engineer"
   - Выберите **Public** или **Private**
   - **НЕ** ставьте галочки на "Add a README file", "Add .gitignore", "Choose a license" (у нас уже есть файлы)
5. Нажмите **"Create repository"**

## Шаг 4: Подключение локального репозитория к GitHub

GitHub покажет инструкции. Выполните команды (замените `YOUR_USERNAME` на ваш GitHub username):

```bash
cd c:\Users\35191\Presentation
git remote add origin https://github.com/YOUR_USERNAME/qa-engineer-presentation.git
git branch -M main
git push -u origin main
```

Если вы используете SSH (и настроили SSH ключи):

```bash
git remote add origin git@github.com:YOUR_USERNAME/qa-engineer-presentation.git
git branch -M main
git push -u origin main
```

## Шаг 5: Включение GitHub Pages (опционально)

Чтобы сайт был доступен по ссылке:

1. Перейдите в настройки репозитория на GitHub
2. В меню слева выберите **"Pages"**
3. В разделе **"Source"** выберите:
   - Branch: `main`
   - Folder: `/ (root)`
4. Нажмите **"Save"**
5. Через несколько минут сайт будет доступен по адресу:
   `https://YOUR_USERNAME.github.io/qa-engineer-presentation/`

## Быстрая команда для всех шагов (после настройки git):

```bash
# Настройка git (выполнить один раз)
git config --global user.name "Ваше Имя"
git config --global user.email "ваш.email@example.com"

# Создание коммита
cd c:\Users\35191\Presentation
git commit -m "Initial commit: QA Engineer presentation website"

# Подключение к GitHub (замените YOUR_USERNAME и REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## Полезные команды для будущих обновлений:

```bash
# После изменений в файлах:
git add .
git commit -m "Описание изменений"
git push
```

---

**Примечание:** Если возникнут проблемы с аутентификацией, GitHub может потребовать Personal Access Token вместо пароля. Создайте его в Settings → Developer settings → Personal access tokens → Tokens (classic).