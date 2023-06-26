import pathlib  
import setuptools 

requires = [
	"flake8 > 5.0.3",
	"pytest",
]

HERE = pathlib.Path(__file__).parent
README = (HERE / "readme.md").read_text()

setuptools.setup(
	name="flake8_example",
	license="GPL-2.0 license",
	version="1.0.0",
	description="Плагин flake8 с проверкой на дополнительные стандарты кода, "
		"принятые на проекте VCS",
	author="Debianov",  
	author_email="debianov@inbox.ru",  
	classifiers=[  
		"Programming Language :: Python :: 3.9",  
		"Programming Language :: Python :: 3.10",  
		"Framework :: Flake8",  
	],  
	py_modules=[  
		"flake8_vcs_ext",  
	],  
	install_requires=requires,  
	entry_points={  # The entry poing for running Flake8 plugin
		"flake8.extension": [
			'VCS001 = flake8_vcs_ext:Plugin',
			# 'VCS002 = flake8_vcs_ext:Plugin'
		],  
	},  
)