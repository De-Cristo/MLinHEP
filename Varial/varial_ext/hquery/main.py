import engine


def main(**kws):
    no_session = kws.pop('no_session', False)
    e = engine.HQueryEngine(kws)

    import server  # server should not be imported in backend process
    server.start(e, no_session)

# TODO "reset" -> make everything new
# TODO put git hash of varial on webcreator (find on webcreator init)
# TODO multiple instances: add random token to jug_file path (delete 2w olds)
# TODO add multiple histos e.g. store histos via python, not in json
# TODO CUTFLOW
# TODO hint toggles (on bins vs. low, high / CUTFLOW)
# TODO add multiple histos (toggled form)
# TODO reloading: use ajax instead of full reload
# TODO status from job submitter (warn when only few jobs are running)
# TODO progress bar or (n_done / n_all) statement
# TODO progress: sometimes it hangs until done. Why?
# TODO first make histos for current section, send reload, then others
# TODO lines in plots if selection is applied (improved N-1 feature)
# TODO SGEJobSubmitter: Jobs are killed after 1 hour. Resubmit before that.
# TODO cut efficiency / cutflow plot in map reduce
# TODO histo_form: put width into CSS block
# TODO separate CSS file for all hquery-related fields
# TODO think about pulling everything through GET
# TODO restart backend button