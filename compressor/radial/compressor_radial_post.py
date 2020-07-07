def compressor_radial_post(run, engine, compressor, Compressor):
    '''
        Post-processing calculated radial compressor data
    '''
    from output_results import output_results
    from create_report import create_report
    from edit_pictures import edit_pictures
    from save_results import save_results
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    output_results(compressor, Compressor)

    create_report(run, engine, compressor, Compressor)

    edit_pictures(compressor, Compressor)

    save_results(compressor)


# ''' (C) 2018-2020 Stanislau Stasheuski '''