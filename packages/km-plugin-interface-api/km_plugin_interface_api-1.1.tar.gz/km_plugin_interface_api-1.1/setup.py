from setuptools import setup, find_packages

setup(name='km-plugin-interface-api',
      version='1.1',
      install_requires=[
          'km-sdk',
          'requests',
      ],
      entry_points={
          "knowledge_management_plugin": [
              'INTERFACE = km_plugin_interface_api.interface_api:InterfaceApi'
          ]
      },
      packages=find_packages(),
      description='知识管理系统插件-通用API对接',
      author='KnowledgeManagement',
      )
