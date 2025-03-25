# highlight.js
cdnjs = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/'



def parse_instrument(input, *args):
    """
    Parse instrumental configuration from front-end to back-end.
    Ensure that only the requested parameters are a valid configuration.

    # 'instrument', 'mode',
    # 'aperture', 'disperser', 'filter', 'subarray', 'readout'
    # 'order', 'ngroup', 'nint', 'detector'
    """
    # instrument and mode always checked
    inst = input.instrument.get().lower()
    mode = input.mode.get()
    detector = get_detector(inst, mode, detectors)
    if detector is None:
        return None

    config = {
        'instrument': inst,
        'mode': mode,
        'detector': detector,
    }

    if 'aperture' in args:
        aperture = input.aperture.get()
        has_pupils = mode in ['lw_ts', 'sw_ts']
        if has_pupils and aperture not in detector.pupils:
            return None
        if not has_pupils and aperture not in detector.apertures:
            return None
        if has_pupils:
            aperture = detector.pupil_to_aperture[aperture]
        config['aperture'] = aperture

    if 'disperser' in args:
        disperser = input.disperser.get()
        if disperser not in detector.dispersers:
            return None
        config['disperser'] = disperser

    if 'filter' in args:
        filter = input.filter.get()
        if filter not in detector.filters:
            return None
        config['filter'] = filter

    if 'subarray' in args:
        subarray = input.subarray.get()
        if subarray not in detector.subarrays:
            return None

    if 'readout' in args:
        readout = input.readout.get()
        if readout not in detector.readouts:
            return None

    # Now parse front-end to back-end:
    if mode == 'target_acq':
        ngroup = int(input.ngroup_acq.get())
        config['disperser'] = None
    else:
        ngroup = input.ngroup.get()
    config['ngroup'] = ngroup

    config['nint'] = 1 if mode == 'target_acq' else input.integrations.get()

    if mode == 'mrs_ts':
        config['aperture'] = ['ch1', 'ch2', 'ch3', 'ch4']

    if mode == 'bots':
        config['disperser'], config['filter'] = filter.split('/')

    if 'order' in args:
        if mode == 'soss':
            if filter == 'f277w':
                order = [1]
            else:
                order = input.order.get()
                order = [int(val) for val in order.split()]
        else:
            order = None
        config['order'] = order

    # Return in the same order as requested
    config_list = [config[arg] for arg in args]

    return config_list


    def update_subarray():
        config = is_consistent2(
            input, 'mode', 'aperture', 'disperser', 'filter', 'detector'
        )
        if config is None:
            return
        mode, aper, disperser, filter, detector = config

        if mode in ['sw_tsgrism', 'sw_ts']:
            constraint = {'aperture': aper}
        else:
            constraint = {'disperser': disperser}
        choices = detector.get_constrained_val('subarrays', **constraint)

        subarray = input.subarray.get()
        if subarray not in choices:
            subarray = detector.default_subarray
        if subarray not in choices:
            subarray = list(choices)[0]
        ui.update_select('subarray', choices=choices, selected=subarray)

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def app():
    # Syntax highlighting
    ui.HTML(
        f'<link rel="stylesheet" href="{cdnjs}styles/base16/one-light.min.css">'
        f'<script src="{cdnjs}highlight.min.js"></script>'
    ),

def server():
    @reactive.effect
    @reactive.event(input.export_button)
    def export_to_notebook():
        (inst, mode, aperture, disperser, filter, subarray, readout, order,
            ngroup, nint) = parse_instrument(input)
        req_saturation = saturation_fraction.get()
        name = input.target.get()
        obs_geometry = input.obs_geometry.get()
        transit_dur = float(input.t_dur.get())
        planet_model_type, depth_label, rprs_sq, teq_planet = parse_obs(input)
        print(planet_model_type)

        target_focus = input.target_focus.get()
        if target_focus == 'acquisition':
            selected = acquisition_targets.cell_selection()['rows'][0]
            target_list = acq_target_list.get()
            target_acq_mag = np.round(target_list[1][selected], 3)
        elif target_focus == 'science':
            #in_transit_integs, in_transit_time = jwst.bin_search_exposure_time(
            #    inst, subarray, readout, ngroup, transit_dur,
            #)
            target_acq_mag = None

        sed_type, sed_model, norm_band, norm_mag, sed_label = parse_sed(
            input, target_acq_mag=target_acq_mag,
        )

        # WRITE SCRIPT
        script = export_script_fixed(inst, mode, aperture, disperser, filter, subarray, readout, order,
            ngroup, nint, sed_type, sed_model, norm_band, norm_mag, sed_label,
            name, obs_geometry, transit_dur, req_saturation)
        #script = 'exported script'


        clipboard.set(script)
        m = ui.modal(
            ui.p("TSO script/notebook"),
            ui.input_action_button(
                id='copy_to_clipboard',
                label='Copy to clipboard',
                class_='btn btn-outline-primary',
            ),
            ui.navset_card_tab(
                ui.nav_panel(
                    "Fixed values",
                    ui.HTML(
                        f'<pre><code class="language-python">{script}</code></pre>'
                        "<script>hljs.highlightAll();</script>"
                    ),
                ),
                ui.nav_panel(
                    "Calculated values",
                    "Panel B content",
                ),
                id="selected_navset_card_tab",
            ),
            easy_close=True,
            size='l',
        )
        ui.modal_show(m)


def export_script_fixed(inst, mode, aperture, disperser, filter, subarray, readout, order,
        ngroup, nint, sed_type, sed_model, norm_band, norm_mag, sed_label,
        name, obs_geometry, transit_dur, req_saturation,
    ):
    # WRITE SCRIPT
    script = f"""\
    import gen_tso.pandeia_io as jwst
    import gen_tso.catalogs as cat
    import numpy as np


    # The Pandeia instrumental configuration:
    instrument = {repr(inst)}
    mode = {repr(mode)}
    pando = jwst.PandeiaCalculation(instrument, mode)

    disperser = {repr(disperser)}
    filter = {repr(filter)}
    subarray = {repr(subarray)}
    readout = {repr(readout)}
    aperture = {repr(aperture)}
    order = {repr(order)}

    # The star:
    sed_type = {repr(sed_type)}
    sed_model = {repr(sed_model)}
    norm_band = {repr(norm_band)}
    norm_mag = {norm_mag}
    pando.set_scene(sed_type, sed_model, norm_band, norm_mag)

    # Integration timings:
    ngroup = {ngroup}
    nint = {repr(nint)}
    # Automate ngroup below requested saturation fraction:
    # ngroup = pando.saturation_fraction(fraction={req_saturation:.1f})

    # Automate nint to match an observation duration:
    # nint, exp_time = jwst.bin_search_exposure_time(
    #     instrument, subarray, readout, ngroup, obs_dur,
    # )

    # Estimate obs_duration:
    # t_base = np.max([0.5*transit_dur, 1.0])
    # obs_dur = t_start + t_settling + transit_dur + 2*t_base
    obs_dur = jwst.obs_duration(transit_dur, t_base)

    # To automate target properties:
    # catalog = cat.Catalog()
    # target = catalog.get_target({repr(name)})
    # t_eff = target.teff
    # logg_star = target.logg_star
    # sed_model = jwst.find_closest_sed(teff, logg_star, sed_type={repr(sed_type)})
    # norm_band = '2mass,ks'
    # norm_mag = target.ks_mag
    # pando.set_scene(sed_type, sed_model, norm_band, norm_mag)\
"""

    if mode == 'target_acq':
        script += """\n
    # Target acquisition
    tso = pando.perform_calculation(
        ngroup, nint, disperser, filter, subarray, readout,
        aperture, order,
    )\
"""
    else:
        script += f"""\n
    # The planet:
    # Planet model: wl(um) and transit depth (no units):
    obs_type = {repr(obs_geometry)}
    spec_file = 'data/models/WASP80b_transit.dat'
    depth_model = np.loadtxt(spec_file, unpack=True)
    depth_label, wl, depth = parse_depth_model(input)
    depth_model = [wl, depth]

    # in-transit and total observation duration times (hours):
    # transit_dur = target.transit_dur
    transit_dur = {transit_dur}
    exp_time = jwst.exposure_time(instrument, subarray, readout, ngroup, nint)
    obs_dur = exp_time / 3600.0

    # Automate obs_duration:
    # t_start = 1.0
    # t_settling = 0.75
    # t_base = np.max([0.5*transit_dur, 1.0])
    # obs_dur = t_start + t_settling + transit_dur + 2*t_base

    # Run TSO simulation:
    tso = pando.tso_calculation(
        obs_type, transit_dur, obs_dur, depth_model,
        ngroup, disperser, filter, subarray, readout, aperture, order,
    )\
"""
    return script

def export_script_calc():
    pass

