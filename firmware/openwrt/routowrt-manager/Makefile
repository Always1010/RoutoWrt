include $(TOPDIR)/rules.mk

PKG_NAME:=routowrt-manager
PKG_VERSION:=1.0.0
PKG_RELEASE:=1
PKG_LICENSE:=MIT
PKGARCH:=all

include $(INCLUDE_DIR)/package.mk

define Package/routowrt-manager
  SECTION:=net
  CATEGORY:=Network
  TITLE:=RoutoWrt transactional configuration manager
  DEPENDS:=+routowrt-core +routowrt-forwarding +rpcd-mod-ucode +ucode +ucode-mod-fs +ucode-mod-digest +uclient-fetch +ca-bundle
endef

define Package/routowrt-manager/conffiles
/etc/routowrt/
endef

define Build/Compile
endef

define Package/routowrt-manager/install
	$(INSTALL_DIR) $(1)/usr/share/ucode/routowrt $(1)/usr/share/rpcd/ucode $(1)/usr/share/rpcd/acl.d $(1)/usr/libexec $(1)/etc/init.d $(1)/etc/uci-defaults
	$(INSTALL_DATA) ./files/usr/share/ucode/routowrt/*.uc $(1)/usr/share/ucode/routowrt/
	$(INSTALL_DATA) ./files/usr/share/rpcd/ucode/routowrt $(1)/usr/share/rpcd/ucode/
	$(INSTALL_DATA) ./files/usr/share/rpcd/acl.d/routowrt.json $(1)/usr/share/rpcd/acl.d/
	$(INSTALL_BIN) ./files/usr/libexec/routowrt-* $(1)/usr/libexec/
	$(INSTALL_BIN) ./files/etc/init.d/routowrt $(1)/etc/init.d/
	$(INSTALL_BIN) ./files/etc/uci-defaults/95-routowrt-schedule $(1)/etc/uci-defaults/
endef

$(eval $(call BuildPackage,routowrt-manager))
