
"use strict";

let Takeoff = require('./Takeoff.js')
let NotifySetpointsStop = require('./NotifySetpointsStop.js')
let SetGroupMask = require('./SetGroupMask.js')
let GoTo = require('./GoTo.js')
let Land = require('./Land.js')
let UpdateParams = require('./UpdateParams.js')
let UploadTrajectory = require('./UploadTrajectory.js')
let Stop = require('./Stop.js')
let StartTrajectory = require('./StartTrajectory.js')

module.exports = {
  Takeoff: Takeoff,
  NotifySetpointsStop: NotifySetpointsStop,
  SetGroupMask: SetGroupMask,
  GoTo: GoTo,
  Land: Land,
  UpdateParams: UpdateParams,
  UploadTrajectory: UploadTrajectory,
  Stop: Stop,
  StartTrajectory: StartTrajectory,
};
