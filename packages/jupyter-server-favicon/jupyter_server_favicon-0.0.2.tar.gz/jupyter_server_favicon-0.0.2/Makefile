.PHONY: build release all clean bump-patch

clean:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

build:
	python -m build --sdist --wheel .
	ls -l dist

release:
	python -m twine upload dist/*

bump-patch:
	$(eval CURRENT_VERSION := $(shell grep -o 'version="[0-9]\+\.[0-9]\+\.[0-9]\+"' setup.py | cut -d'"' -f2))
	$(eval MAJOR := $(shell echo $(CURRENT_VERSION) | cut -d. -f1))
	$(eval MINOR := $(shell echo $(CURRENT_VERSION) | cut -d. -f2))
	$(eval PATCH := $(shell echo $(CURRENT_VERSION) | cut -d. -f3))
	$(eval NEW_PATCH := $(shell echo $$(($(PATCH) + 1))))
	$(eval NEW_VERSION := $(MAJOR).$(MINOR).$(NEW_PATCH))
	@echo "Bumping version from $(CURRENT_VERSION) to $(NEW_VERSION)"
	python -m tbump $(NEW_VERSION)

all: clean bump-patch build release
