;; we set up python shell to use the project virtual environment
;; python lsp, etc. will use our default python interpreter, set up with uv
((nil
  (python-shell-process-environment . ("DJANGO_SETTINGS_MODULE=people.settings"))
  (python-shell-extra-pythonpaths . ("/Users/adrianflanagan/Devel/personal/people/app/people/"))
  (python-shell-virtualenv-root . "/Users/adrianflanagan/Devel/personal/people/app/.venv/")))
