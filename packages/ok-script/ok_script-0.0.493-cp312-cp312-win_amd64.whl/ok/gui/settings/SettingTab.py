# coding:utf-8
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from qfluentwidgets import (SettingCardGroup, ComboBoxSettingCard)

from ok import og
from ok.gui.common.config import cfg
from ok.gui.settings.GlobalConfigCard import GlobalConfigCard
from ok.gui.widget.Tab import Tab


class SettingTab(Tab):
    """ Setting interface """

    def __init__(self):
        super().__init__()
        self.personalGroup = SettingCardGroup(
            self.tr('Personalization'))
        self.vBoxLayout.addWidget(self.personalGroup)

        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr('Language'),
            self.tr('Set your preferred language'),
            texts=['简体中文', 'English', self.tr('Use system setting')],
            parent=self.personalGroup
        )
        self.config_groups = []
        self.app_group = None
        self.__initWidget()

    def __initWidget(self):
        self.__initLayout()
        self.add_global_config()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.languageCard)

    def goto_config(self, key):
        to_scroll = None
        for config in self.config_groups:
            if config.has_key(key):
                config.setExpand(True)
                to_scroll = config
            else:
                config.setExpand(False)
        # if to_scroll:
        #     self.scroll()

    def add_global_config(self):
        global_configs = og.executor.global_config.get_all_visible_configs()
        if global_configs:
            self.app_group = SettingCardGroup(
                self.tr('App Settings'))
            for name, config, option in global_configs:
                card = GlobalConfigCard(config, option)
                self.app_group.addSettingCard(card)
                self.config_groups.append(card)
            self.vBoxLayout.addWidget(self.app_group)

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.success(
            self.tr('Updated successfully'),
            self.tr('Configuration takes effect after restart'),
            duration=1500,
            parent=self
        )

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self.__showRestartTooltip)

        # personalization
        # self.themeCard.optionChanged.connect(lambda ci: setTheme(cfg.get(ci)))
