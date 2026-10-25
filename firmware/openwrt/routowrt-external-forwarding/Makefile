include $(TOPDIR)/rules.mk

PKG_NAME:=routowrt-external-forwarding
PKG_VERSION:=1.0.0
PKG_RELEASE:=3
PKG_LICENSE:=MIT GPL-3.0-only
PKGARCH:=all
PKG_FILE_DEPENDS:=$(CURDIR)/payload.json $(CURDIR)/../routowrt-external-manager/tools/stage-files.py $(foreach input,$(shell python3 $(CURDIR)/../routowrt-external-manager/tools/stage-files.py --manifest $(CURDIR)/payload.json --list-sources),$(TOPDIR)/package/$(input))

include $(INCLUDE_DIR)/package.mk

define Package/routowrt-external-forwarding
  SECTION:=net
  CATEGORY:=Network
  TITLE:=RoutoWrt optional external forwarding
  DEPENDS:=+firewall4 +ip-full +ucode +ucode-mod-fs
  CONFLICTS:=routowrt-forwarding routowrt-manager
endef

define Build/Prepare
	python3 $(CURDIR)/../routowrt-external-manager/tools/stage-files.py --manifest $(CURDIR)/payload.json --source-root $(TOPDIR)/package --output $(PKG_BUILD_DIR)/payload
endef

define Build/Compile
endef

define Package/routowrt-external-forwarding/install
	$(CP) $(PKG_BUILD_DIR)/payload/. $(1)/
endef

$(eval $(call BuildPackage,routowrt-external-forwarding))
