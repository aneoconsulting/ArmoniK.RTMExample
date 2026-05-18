# -*- mode: perl -*-
run_name = "Fathi2015_initial_run";

# duration of the run
sim_time = 0.25;
mesh_file = "mesh4spec"; # input mesh file
mat_file = "material.input";
dim=3;

snapshots {
    save_snap = true;
    snap_interval = 0.05;
    select all;
};

# Description des capteurs
save_traces = true;
station_file = "capteurs.dat";

# Fichier protection reprise
prorep=false;
prorep_iter=1000;


# introduce a source
source {
    coords = 0. 0. 0.;
    type = impulse;
    dir = 0. 0. -1.;
    func = file;
    time_file = "source_p20.txt";
};

time_scheme {
    accel_scheme = false;  # Acceleration scheme for Newmark
    veloc_scheme = true;   # Velocity scheme for Newmark
    alpha = 0.5;           # alpha (Newmark parameter)
    beta = -0.5;           # beta (Newmark parameter)
    gamma = 1;             # gamma (Newmark parameter)
    courant=0.2;
};

ngll=5;

amortissement {
    nsolids = 0;           # number of solids for attenuation (0 if no attenuation)
    atn_band = 10  0.05;   # attenuation period band
    atn_period = 0.2;      # model period 
};
