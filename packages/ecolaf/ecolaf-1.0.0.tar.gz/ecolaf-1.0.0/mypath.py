class Path(object):
    @staticmethod
    def db_root_dir(dataset):
        if dataset == 'DELIVER':
            return '/home/lderegnaucourt/data/DELIVER/'
        elif dataset == 'MUSES' or dataset == 'MUSES_CLEAR':
            return 'home/lderegnaucourt/data/MUSES/'
        else:
            print('Dataset {} not available.'.format(dataset))
            raise NotImplementedError
