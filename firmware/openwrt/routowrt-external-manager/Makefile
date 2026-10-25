include $(TOPDIR)/rules.mk

PKG_NAME:=routowrt-external-manager
PKG_VERSION:=1.0.0
PKG_RELEASE:=6
PKG_LICENSE:=MIT GPL-3.0-only
PKGARCH:=all
PKG_FILE_DEPENDS:=$(CURDIR)/payload.json $(CURDIR)/../routowrt-external-manager/tools/stage-files.py $(foreach input,$(shell python3 $(CURDIR)/../routowrt-external-manager/tools/stage-files.py --manifest $(CURDIR)/payload.json --list-sources),$(TOPDIR)/package/$(input))

include $(INCLUDE_DIR)/package.mk

define Package/routowrt-external-manager
  SECTION:=net
  CATEGORY:=Network
  TITLE:=RoutoWrt optional external manager
  DEPENDS:=+routowrt-external-forwarding +rpcd-mod-ucode +ucode +ucode-mod-fs +ubus +dnsmasq +busybox
  CONFLICTS:=routowrt-manager routowrt-forwarding
endef

define Package/routowrt-external-manager/conffiles
/etc/routowrt/
endef

define Build/Prepare
	python3 $(CURDIR)/../routowrt-external-manager/tools/stage-files.py --manifest $(CURDIR)/payload.json --source-root $(TOPDIR)/package --output $(PKG_BUILD_DIR)/payload
endef

define Build/Compile
endef

define Package/routowrt-external-manager/install
	$(CP) $(PKG_BUILD_DIR)/payload/. $(1)/
endef

$(eval $(call BuildPackage,routowrt-external-manager))
