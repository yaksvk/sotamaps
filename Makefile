test:
	cd vhf_app; python3 -m unittest
	cd sotamaps_app; python3 -m unittest
	python3 -m unittest

.PHONY: test
