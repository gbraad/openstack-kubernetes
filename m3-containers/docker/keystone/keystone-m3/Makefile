SHELL       := /bin/sh
REPOSITORY  := hub.global.cloud.sap/monsoon/ubuntu-source-keystone-m3
TAG         ?= latest
IMAGE       := $(REPOSITORY):$(TAG)

### Executables
DOCKER      = docker
WAIT        = $(DOCKER) run --rm --link $(WAIT_ID):wait $(WAIT_OPTS) docker.mo.sap.corp/monsoon-docker/wait || ($(DOCKER) logs $(WAIT_ID) && false)

# ----------------------------------------------------------------------------------
#   image
# ----------------------------------------------------------------------------------
image: build
	echo $(IMAGE) > image

# ----------------------------------------------------------------------------------
#   build
# ----------------------------------------------------------------------------------
#
# Build and tags an image from a Dockerfile.
#
# We need to reset the modification times of all files in a git repository to the
# date of the latest commit that changed it. This is required because Docker takes
# the mtime of a file into account when checking for modifications. Git on the other
# hand does not. Without this the cache will be busted by Git and is basically
# useless.
#
build:
	$(DOCKER) pull $(REPOSITORY):latest || true
	$(DOCKER) build -t $(IMAGE) --rm .
	echo $(IMAGE) > build

# ----------------------------------------------------------------------------------
#   clean
# ----------------------------------------------------------------------------------
#
# Kill and remove all containers. Remove intermediate files.
#
.PHONY:
clean:
	$(DOCKER) rm -f $(postgres) $(webapp) &> /dev/null || true
	$(RM) image build precompile webapp postgres
