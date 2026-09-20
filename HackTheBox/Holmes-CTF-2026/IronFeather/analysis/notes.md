# Iron Feather — Sherlock 07 "Mission Vault" — analysis state

## Artifacts
- `scripts/emulate_kdf.py`, `scripts/decrypt.py` -> `analysis/dataman` (1208528B), `analysis/flight.ulg` (68828059B, magic `ULog\x01`)
- `scripts/parse_dataman.py` -> mission items from bank 0
- `scripts/dump_topic.py analysis/flight.ulg <topic>` -> ulog topics

## Encryption / KDF (done, answers validated by successful decrypt)
- Q1 magic: `PX4DMENC`
- Q2 algo: AES-256-GCM (12B nonce, 16B tag, AAD = 44B header)
- Q3 KDF address: `0x170af0`
- Q4 rounds (custom mixing): `384`
- Q5 standard KDF: PBKDF2-HMAC-SHA256 (iter 8192, salt = file[16:32], dklen 32)
- Q6 AES key: `a40ba87b8a0e21d4ead98b917c4bf0f60cc65b25c614b93f107e5ed1e483d6ce`

## Dataman (PX4 v1.14-style, custom "mission-vault" layout)
- per-item tables from binary: sizes={60,60,12,36,36,12,60,60,44,12}, max={32,32,1,64,64,1,10000,10000,1,1}
- sector = 4-byte header (len) + payload; mission_item_s = 56B, stride 60B
- key6 = mission bank 0 at file offset 0x2118 ; key7 = bank 1 at 0x948D8 (empty)
- bank 0 holds 24 items (0..23) == mission_result.seq_total=24 (NOTE: bank1 also has garbage in its indices region)
  -> Q7 active dataman/bank = 0 ; Q8 mission items = 24
- items (idx: cmd | params | lat/lon/alt):
  0: 22 TAKEOFF   | 51.4997000, -0.1608000, alt 15
  1: 178 DO_CHANGE_SPEED | 4.5
  2-6: 16 NAV_WAYPOINT | survey to (51.50335,-0.16005) alt 26
  7: 178 | 2.2
  8: 16 | (51.50355,-0.16045) alt 12
  9: 16 | (51.5035598,-0.1608362) alt 2, time_inside=3  <== hover/drop point
  10: 187 DO_SET_ACTUATOR | param1=1  <== release (executed 446.656s)
  11: 93 NAV_DELAY | 2s
  12: 187 DO_SET_ACTUATOR | 0
  13: 178 | 4.8
  14-20: 16 NAV_WAYPOINT | back-sweep toward home
  21: 178 | 2
  22: 16 | (51.5001,-0.16086) alt 6
  23: 21 NAV_LAND | (51.49970, -0.16080)
- MISSION_STATE sector at 0x127098: header 0x28 (=40, sizeof mission_s) … timestamp, current_seq=18

## Flight (ulog)
- vehicle_command (ack'd): 211 DO_GRIPPER @0.276s (grab), 176 DO_SET_MODE ext, 400 ARM @285.26s,
  178 speeds, 187 DO_SET_ACTUATOR @446.66s, 420 MAV_CMD_INJECT_FAILURE @520.764s ack OK, 400 DISARM @576.968s
- Q13 injected "bring down" command: MAV_CMD_INJECT_FAILURE (H8/420) @520.764s + mission aborted @522.992s
- Q11 takeoff (home): lat 51.4996985 lon -0.1607997
- Q12 payload release GPS: 51.5035602 -0.1608417 (item 9 hover / actuator @446.6s)
- Q10 landing (item 23 NAV_LAND target): 51.49970 -0.16080
- Q15 crash (disarm @576.968s): 51.5016936 -0.1620924
- Q16 disarm time: 576.968 s (armed->0 transition; command sent 576.956)
- Q14 distances (haversine): takeoff->crash 239 m ; release->injection 224 m ; path release->injection 277 m
- Q17 nearest road to crash: Knightsbridge (OSM reverse geocode, point inside way 744663874)

## Update: crash = IMPACT at ~525.9s (failure injection @520.764 sent it down 67->27 m)
- impact vGPOS (525.856): 51.5016938, -0.1620929
- GPS sensor at 526.016: 51.5016943, -0.1620924
- disarm @576.968, land_detected @577.312
## takeoff variants
- vGPOS@arm 285.256 = home = 51.4996985/ -0.1607997 ; GPS@285.268 51.4996989/-0.1607997 ;
  mission item0 51.4997000/-0.1608000 ; vLP ref 51.4996987/-0.1608002