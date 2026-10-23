include $(TOPDIR)/rules.mk

PKG_NAME:=routowrt-core
PKG_VERSION:=1.13.21
PKG_RELEASE:=1
PKG_LICENSE:=GPL-3.0-or-later
PKG_FILE_DEPENDS:=$(TOPDIR)/routowrt-input/sing-box \
	$(TOPDIR)/routowrt-input/build-info.json \
	$(TOPDIR)/routowrt-input/LICENSE

include $(INCLUDE_DIR)/package.mk

# Preserve the exact externally built and device-tested ELF payload.
RSTRIP:=:

define Package/routowrt-core
  SECTION:=net
  CATEGORY:=Network
  TITLE:=RoutoWrt static sing-box evaluation core
  DEPENDS:=+ca-bundle +kmod-nft-tproxy +ip-full
endef

define Package/routowrt-core/description
  Fixed, externally built static sing-box core for the selected target.
  Image inspection must verify its CPU architecture and reviewed provenance.
  This evaluation package does not enable forwarding or install a proxy UI.
endef

define Build/Prepare
	$(INSTALL_DIR) $(PKG_BUILD_DIR)
	$(CP) $(TOPDIR)/routowrt-input/sing-box $(PKG_BUILD_DIR)/sing-box
	$(CP) $(TOPDIR)/routowrt-input/build-info.json $(PKG_BUILD_DIR)/build-info.json
	$(CP) $(TOPDIR)/routowrt-input/LICENSE $(PKG_BUILD_DIR)/LICENSE
endef

define Build/Compile
endef

define Package/routowrt-core/install
	$(INSTALL_DIR) $(1)/usr/bin $(1)/usr/share/routowrt
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/sing-box $(1)/usr/bin/sing-box
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/build-info.json $(1)/usr/share/routowrt/build-info.json
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/LICENSE $(1)/usr/share/routowrt/LICENSE
endef

$(eval $(call BuildPackage,routowrt-core))
