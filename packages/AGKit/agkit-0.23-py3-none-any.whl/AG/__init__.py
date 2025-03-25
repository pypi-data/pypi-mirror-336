from AG.INI import INI
from AG.Logger import Logger
from AG.Template import Template

Logger()
INI().Instance.Init("config")
Template().Instance.Init("Template")
