# ADHD Reset Planner — build pipeline
# Usage:  make all   (from the adhd-planner/ directory, with the venv active)
#
# One-time setup:
#   python3 -m venv ../.venv-planner && . ../.venv-planner/bin/activate \
#     && pip install -r requirements.txt

PY = python
SRC = src

.PHONY: all planner docs stickers verify package clean

all: planner docs stickers verify package

planner:            ## build light + dark planner PDFs
	$(PY) $(SRC)/build.py
	$(PY) $(SRC)/build.py --dark

docs:               ## build the branded Start-Here.pdf
	$(PY) $(SRC)/build_docs.py

stickers:           ## generate transparent sticker PNGs + sheet
	cd $(SRC) && $(PY) make_stickers.py

verify:             ## confirm every internal link resolves
	cd $(SRC) && $(PY) verify_links.py ../build/adhd-planner-light.pdf
	cd $(SRC) && $(PY) verify_links.py ../build/adhd-planner-dark.pdf

package:            ## assemble dist/ bundle + customer zip
	mkdir -p dist/stickers
	cp build/adhd-planner-light.pdf dist/ADHD-Reset-Planner-Light.pdf
	cp build/adhd-planner-dark.pdf  dist/ADHD-Reset-Planner-Dark.pdf
	cp assets/stickers/good-stamp.png assets/stickers/okay-stamp.png \
	   assets/stickers/good-dot.png assets/stickers/okay-dot.png \
	   assets/stickers/sticker-sheet.pdf dist/stickers/
	cd dist && rm -f ADHD-Reset-Planner.zip && \
	  zip -rq ADHD-Reset-Planner.zip ADHD-Reset-Planner-Light.pdf \
	  ADHD-Reset-Planner-Dark.pdf Start-Here.pdf README.md VIDEO-SCRIPT.md stickers
	@echo "packaged -> dist/ADHD-Reset-Planner.zip"

clean:
	rm -rf build/*.pdf build/preview dist/*.pdf dist/*.zip dist/stickers
