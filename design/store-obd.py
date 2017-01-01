# Copyright 2016 Timothy M. Shead
#
# This file is part of Pipecat.
#
# Pipecat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pipecat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pipecat.  If not, see <http://www.gnu.org/licenses/>.

import obd

import pipecat.device.auto
import pipecat.record
import pipecat.store.pickle

pipe = obd.OBD("/dev/cu.SLAB_USBtoUART")
pipe = pipecat.device.auto.obd(pipe)
pipe = pipecat.store.pickle.write(pipe, "../data/obd.pickle")
for record in pipe:
    pipecat.record.dump(record)

