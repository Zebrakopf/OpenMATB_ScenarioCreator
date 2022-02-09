
#define difficulty differences
easy = {"lossA"          : 1000, #loss per minute of tank A
            "lossB"         : 1000, #loss per minute of tank A
            "flowStd"       : 1000, #flow from bottom tanks to top
            "flowBetween"   : 500, # flow from main tank connections
            "tankTolerance" : 300, #tolerance zone of both tanks
            "pumpFailN"     : 15, # number of pump failures
            "promptN"       : 5, #number of comm prompts
            "trackingRad"   : 0.3, # safezone of the tracking task
            "sysSafe"       : 2, # default jitter of the gages
            "scaleFailN"    : 10, # number of scale failures
            "scalesToFail"  : [1,2], # scales that can fail
            "pumpsToFail"   : [1,2,3,4,5,6,7,8], # pumps that can fail
            "safeZone"      : 2 #change this to have events overlap more
}
medium = {"lossA"          : 1000,
            "lossB"         : 1000,
            "flowStd"       : 600, #flow now doesn't match the loss rate anymore -> more strategising needed
            "flowBetween"   : 400, # same as above. The inbetween now have to be used to keep the tanks happy
            "tankTolerance" : 300, # tolerance is slighlty lower -> need to keep a better eye on the tanks
            "pumpFailN"     : 15, # more failures
            "promptN"       : 7, # slightly more prompts
            "trackingRad"   : 0.2, # smaller tracking radius -> affords more attention now
            "sysSafe"       : 3, # more default jitter in the gages -> may catch attention when none is needed
            "scaleFailN"    : 15, # more scale failures
            "scalesToFail"  : [1,2,3,4], # more scales may fail now -> more buttons to manage
            "pumpsToFail"   : [1,2,3,4,5,6,7,8], # nothing has changed here
            "safeZone"      : 2 #nothing has changed here
}
hard = {"lossA"          : 1300, # lossrate is now increased -> easier to fall out of tolerance zone
            "lossB"         : 1300, # lossrate is now increased -> easier to fall out of tolerance zone
            "flowStd"       : 1000, # flow rate is also increased and doesn't match loss rate -> same as above
            "flowBetween"   : 1000, # flow rate is also increased and doesn't match loss rate -> same as above
            "tankTolerance" : 300, # tolerance lowered again
            "pumpFailN"     : 20, # even more pump failures
            "promptN"       : 10, # even more comm prompts
            "trackingRad"   : 0.15, # tracking radius even smaller
            "sysSafe"       : 4, # jtter increased again
            "scaleFailN"    : 20, # even more scale failures
            "scalesToFail"  : [1,2,3,4], # unchanged from medium (could add the top two lights here)
            "pumpsToFail"   : [1,2,3,4,5,6], # the inbetween pumps cannot fail anymore -> bottom pumps will fail more often and reliance of inbetween pumps increases
            "safeZone"      : 2 #nothing has changed here
}
