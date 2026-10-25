include $(TOPDIR)/rules.mk

PKG_NAME:=luci-app-routowrt-external
PKG_VERSION:=1.0.0
PKG_RELEASE:=3
PKG_LICENSE:=MIT GPL-3.0-only
PKGARCH:=all
PKG_FILE_DEPENDS:=$(CURDIR)/payload.json $(CURDIR)/../routowrt-external-manager/tools/stage-files.py $(foreach input,$(shell python3 $(CURDIR)/../routowrt-external-manager/tools/stage-files.py --manifest $(CURDIR)/payload.json --list-sources),$(TOPDIR)/package/$(input))

include $(INCLUDE_DIR)/package.mk

define Package/luci-app-routowrt-external
  SECTION:=net
  CATEGORY:=Network
  TITLE:=RoutoWrt optional external LuCI
  DEPENDS:=+luci-base +routowrt-external-manager
  CONFLICTS:=luci-app-routowrt
endef

define Build/Prepare
	python3 $(CURDIR)/../routowrt-external-manager/tools/stage-files.py --manifest $(CURDIR)/payload.json --source-root $(TOPDIR)/package --output $(PKG_BUILD_DIR)/payload
endef

define Build/Compile
endef

define Package/luci-app-routowrt-external/install
	$(CP) $(PKG_BUILD_DIR)/payload/. $(1)/
endef

# Match LuCI's normal package cache refresh; no service activation.
define Package/luci-app-routowrt-external/postinst
[ -n "$${IPKG_INSTROOT}" ] || { \
	rm -f /tmp/luci-indexcache.*; \
	/etc/init.d/rpcd reload 2>/dev/null; \
	exit 0; \
}
endef

$(eval $(call BuildPackage,luci-app-routowrt-external))
