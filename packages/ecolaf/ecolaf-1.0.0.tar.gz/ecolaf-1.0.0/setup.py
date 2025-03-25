from setuptools import setup

######################################################################################################
################ You May Remove All the Comments Once You Finish Modifying the Script ################
######################################################################################################

setup(

    name = 'ecolaf', 
    
    version = '1.0.0',
    
    description = 'A toolkit python package to build an adaptive multimodal late fusion pipeline based on Dempster-Shafer Theory for semantic segmentation and classification tasks.',
    
    py_modules = ["ecolaf", "Dempster_Shafer_utils"],

    package_dir = {'':'src'},
    
    author = 'Lucas Deregnaucourt',
    author_email = 'lucas.deregnaucourt@insa-rouen.fr',
    
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    long_description_content_type = "text/markdown",
    
    url='https://github.com/deregnaucourtlucas/ECOLAF',
    
    include_package_data=True,

    install_requires = [

        'torch'

    ],
    
    keywords = ['Dempster-Shafer Theory', 'Deep Learning', 'Multimodal', 'Semantic Segmentation', 'Classification'],
    
)
