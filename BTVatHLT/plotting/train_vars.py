import numpy as np

time_information = ['Event_time', 'Cpfcan_time', 'Jet_time', 'Jet_vertex_time', 'PUrho']
csv_information = ['pfDeepCSVJetTags_probb']
track_information = ['trackSip3dVal']

plot_configs = {
    'Event_time'                   : {"bins": np.linspace(-0.8, 0.8, 20)   , "log": False ,    "underflow": -1.  },
    'Cpfcan_time'                  : {"bins": np.linspace(0., 1.0, 30)     , "log": True  ,    "underflow": -1.  },
    'Jet_time'                     : {"bins": np.linspace(0., 0.99, 30)    , "log": True  ,    "overflow" :  1.  },
    'Jet_vertex_time'              : {"bins": np.linspace(0., 0.99, 30)    , "log": True  ,    "overflow" :  1.  },
    'PUrho'                        : {"bins": np.linspace(0., 5.0, 50)     , "log": False ,                      },
    'pfDeepCSVJetTags_probb'       : {"bins": np.linspace(0., 1.0, 30)     , "log": False ,    "underflow": -1.  },
    'trackSip3dVal'                : {"bins": np.linspace(-0.8, 0.8, 20)   , "log": True  ,                      },
}

label_n_masks = {
    'B' : ['isB'],
    'UDSG' : ['isUD','isS','isG'],
}