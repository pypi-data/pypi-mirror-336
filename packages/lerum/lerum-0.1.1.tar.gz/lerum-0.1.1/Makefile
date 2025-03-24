.PHONY: sync
sync:
	@uv sync --all-packages


.PHONY: publish
publish:
	# +$(MAKE) -C packages/lerum-cli build
	@uv build --all-packages
	# @uv publish