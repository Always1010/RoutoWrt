include $(TOPDIR)/rules.mk

PKG_NAME:=routowrt-forwarding
PKG_VERSION:=1
PKG_RELEASE:=1
PKG_LICENSE:=MIT
PKGARCH:=all

include $(INCLUDE_DIR)/package.mk

define Package/routowrt-forwarding
  SECTION:=net
  CATEGORY:=Network
  TITLE:=RoutoWrt LAN forwarding adapter
  DEPENDS:=+routowrt-core +firewall4 +jsonfilter +ip-full +ubus
endef

define Build/Compile
endef

define Package/routowrt-forwarding/install
	$(INSTALL_DIR) $(1)/usr/libexec
	$(INSTALL_BIN) ./files/routowrt-forwarding $(1)/usr/libexec/routowrt-forwarding
endef

$(eval $(call BuildPackage,routowrt-forwarding))
