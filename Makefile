.PHONY: clean prepare dist release create-release upload

PYCACHE := $(shell find . -name '__pycache__')
EGGS := $(wildcard *.egg-info)
CURRENT_VERSION := $(shell awk '/version =/ {print substr($$3, 2, length($$3)-2)}' pyproject.toml)

clean:
	@echo "=> Cleaning"
	@rm -fr build dist $(EGGS) $(PYCACHE)

prepare: clean
	git add .
	git status
	git commit -m "cleanup before release"

dist: clean
	@python -m build -n
	@ls -l dist/


release:
	git add .
	git status
	git diff-index --quiet HEAD || git commit -m "Latest release: $(CURRENT_VERSION)"
	git tag -a v$(CURRENT_VERSION) -m "Latest release: $(CURRENT_VERSION)"
	
create-release:
	@git push
	@git push --tags
	@gh release create v$(CURRENT_VERSION) \
		dist/bd_materials-$(CURRENT_VERSION)-py3-none-any.whl \
		dist/bd_materials-$(CURRENT_VERSION).tar.gz \
		--title "bd_materials-$(CURRENT_VERSION)" \
		--notes "v$(CURRENT_VERSION)" \
		--target main

upload:
	@twine upload dist/*
