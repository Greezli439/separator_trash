from setuptools import setup, find_namespace_packages
 
setup(
      name = 'clean_folder_test_28.01.23',
      version = '1.0.8',
      description = 'Trash separator from path',
      url = 'https://github.com/Greezli439/separator_trash',
      author = 'Mykhailo',
      author_email = 'greezli439@gmail.com',
      license = 'Apache License',
      packages = find_namespace_packages(),
      include_package_data = True,
      entry_points = {'console_scripts': ['arrange_my_dir = src.clean_folder_test_goit.clean:arrange_dir']}
      )
