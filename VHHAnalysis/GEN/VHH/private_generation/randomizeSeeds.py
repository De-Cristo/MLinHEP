def randomizeSeeds(process):
    from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
    rndSvc=RandomNumberServiceHelper(process.RandomNumberGeneratorService)
    rndSvc.populate()
    return process