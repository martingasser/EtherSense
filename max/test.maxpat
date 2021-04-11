{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 8,
			"minor" : 1,
			"revision" : 8,
			"architecture" : "x64",
			"modernui" : 1
		}
,
		"classnamespace" : "box",
		"rect" : [ 70.0, 784.0, 1690.0, 789.0 ],
		"bglocked" : 0,
		"openinpresentation" : 0,
		"default_fontsize" : 12.0,
		"default_fontface" : 0,
		"default_fontname" : "Arial",
		"gridonopen" : 1,
		"gridsize" : [ 15.0, 15.0 ],
		"gridsnaponopen" : 1,
		"objectsnaponopen" : 1,
		"statusbarvisible" : 2,
		"toolbarvisible" : 1,
		"lefttoolbarpinned" : 0,
		"toptoolbarpinned" : 0,
		"righttoolbarpinned" : 0,
		"bottomtoolbarpinned" : 0,
		"toolbars_unpinned_last_save" : 0,
		"tallnewobj" : 0,
		"boxanimatetime" : 200,
		"enablehscroll" : 1,
		"enablevscroll" : 1,
		"devicewidth" : 0.0,
		"description" : "",
		"digest" : "",
		"tags" : "",
		"style" : "",
		"subpatcher_template" : "",
		"assistshowspatchername" : 0,
		"boxes" : [ 			{
				"box" : 				{
					"basictuning" : 440,
					"data" : 					{
						"clips" : [ 							{
								"absolutepath" : "Macintosh HD:/Users/martin/devel/MagicQueen/vcstereo/11_vc_kontaktstelle4.wav",
								"filename" : "11_vc_kontaktstelle4.wav",
								"filekind" : "audiofile",
								"id" : "u616005360",
								"loop" : 1,
								"content_state" : 								{
									"loop" : 1
								}

							}
 ]
					}
,
					"followglobaltempo" : 0,
					"formantcorrection" : 0,
					"id" : "obj-44",
					"maxclass" : "playlist~",
					"mode" : "basic",
					"numinlets" : 1,
					"numoutlets" : 5,
					"originallength" : [ 0.0, "ticks" ],
					"originaltempo" : 120.0,
					"outlettype" : [ "signal", "signal", "signal", "", "dictionary" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 1364.0, 50.0, 150.0, 30.0 ],
					"pitchcorrection" : 0,
					"quality" : "basic",
					"timestretch" : [ 0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-41",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 458.0, 468.0, 203.0, 22.0 ],
					"text" : "expr ($f1+3.1415927)/(2*3.1415927)"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-40",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 1132.0, 35.0, 96.0, 22.0 ],
					"text" : "\"Slope: Rate\" $1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-39",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 0,
					"patching_rect" : [ 1013.0, 709.0, 96.285714285714221, 22.0 ],
					"text" : "dac~"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-34",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 218.0, 512.0, 203.0, 22.0 ],
					"text" : "expr ($f1+3.1415927)/(2*3.1415927)"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-16",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 1013.0, 35.0, 107.0, 22.0 ],
					"text" : "\"Slope: Center\" $1"
				}

			}
, 			{
				"box" : 				{
					"autosave" : 1,
					"bgmode" : 0,
					"border" : 0,
					"clickthrough" : 0,
					"id" : "obj-10",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 8,
					"offset" : [ 0.0, 0.0 ],
					"outlettype" : [ "signal", "signal", "", "list", "int", "", "", "" ],
					"patching_rect" : [ 1013.0, 107.5, 560.0, 552.0 ],
					"save" : [ "#N", "vst~", "loaduniqueid", 0, "C74_AU:/Venom", ";" ],
					"saved_attribute_attributes" : 					{
						"valueof" : 						{
							"parameter_invisible" : 1,
							"parameter_longname" : "vst~[1]",
							"parameter_shortname" : "vst~[1]",
							"parameter_type" : 3
						}

					}
,
					"saved_object_attributes" : 					{
						"parameter_enable" : 1,
						"parameter_mappable" : 0
					}
,
					"snapshot" : 					{
						"filetype" : "C74Snapshot",
						"version" : 2,
						"minorversion" : 0,
						"name" : "snapshotlist",
						"origin" : "vst~",
						"type" : "list",
						"subtype" : "Undefined",
						"embed" : 1,
						"snapshot" : 						{
							"pluginname" : "Venom.auinfo",
							"plugindisplayname" : "Venom",
							"pluginsavedname" : "C74_AU:/Venom",
							"pluginsaveduniqueid" : 1449487983,
							"version" : 1,
							"isbank" : 0,
							"isbase64" : 1,
							"sliderorder" : [  ],
							"slidervisibility" : [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
							"blob" : "1328.hAGaoMGcv.C1AHv.DTfAGfPBJrvDTTgEWvUag4VclE1XzUmbkIGUjEFcgwUYrUVak4Fcs3VXsU1UyUmXzkGbkckckI2bo8laTQWdvU1WP7fZ0MVYPwVcmklaSQWXzUFUtEVakIwUgAmbOAAw..............vE..PCA+C......zfv........ML7Oa0ls..PCDC.......zPw+.......MXL.......PCGC.......z.x+.H.....MjL......DfpO9Cf....AnJj+.....P.pF4O.B...DfpR9C.....An5j+.H...P.pR4O.....DfpU9C.....Anpk+.H...P.pdoO.B...Dfpt9SFuEG.An5q+jwawAP.pBK......Dfpw5Cf....Anpr9vLyMKMCM3PDQESTxD8CPDELUkjavUGcQ+fDV8TczAWczIgUk41aP.fDgUmY38TDCnmUCISHwM...vyTPUDVXARcyU1QL0iHvHBHsUGazkFcnIWYgQVZtcVOh.iHfLFZgkla8HBQA0DTI4zQrPTQCETVrXTQAoUQrXzSCU0TrzTRRI0SRwBTIQ0PHwxTL8DTEIBHvIWYyUFcNEVak0iHDUlYgUGazIBHyUFakMFckQVQlYVYiQWOhHhO7.UPRETSfjFY8HBbwHBH1EFa0UVOhDiKvbyL0TCLvLyL0XSNyLiMkEiHu3COPEjTA0DHoQVOh.WLvHBH1EFa0UVOhDiHu3COPEjTA0DHoQVOh.WLwHBH1EFa0UVOhbiK1biM4fCM3XyLxfSLxTSYxHxK9vCTAIUPMARZj0iHvEiLh.hcgwVck0iHwHxK9vCTAIUPMARZj0iHvEyLh.hcgwVck0iHx3xLzPCLv.yLyjSMvfCL0bSYsDiHu3COPEjTA0DHoQVOh.WLzHBH1EFa0UVOh.iHu3COPEjTA0DHoQVOh.WL0HBH1EFa0UVOhbiK2LCM4jSN1TiM1byMxPiMk0RLh7hO7.UPRETSfjFY8HBbwXiHfXWXrUWY8HBMtPiMvfCNxfyMyTyL0DSM1TlLh7hO7.UPRETSfjFY8HBbwbiHfXWXrUWY8HBLh7hO7.UPRETSfjFY8HBbwfiHfXWXrUWY8HBNtDSNv.CLv.SM2HiLvPSM4TVKwHxK9vCTAIUPMARZj0iHvIiHfXWXrUWY8HBLh7hO7.UPRETSfjFY8HBbx.iHfXWXrUWY8HRKyHxK9vCTAIUPMARZj0iHvISLh.hcgwVck0iHsLiHu3COPEjTA0DHoQVOh.mLxHBH1EFa0UVOh.iHu3COPEjTA0DHoQVOh.mLyHBH1EFa0UVOhLiHu3COPEjTA0DHoQVOh.mLzHBH1EFa0UVOhHiHu3COPEjTA0DHoQVOh.2Lh.hcgwVck0iH33RN4jSN4jyM1DSM3DCMxDSYsDiHu3COPEjTA0DHoQVOh.GMh.hcgwVck0iHvHxK9vCTAIUPMARZj0iHvUiHfXWXrUWY8HxLkIiHu3COPEjTA0DHoQVOh.mMh.hcgwVck0iHvHxK9vCTAIUPMARZj0iHvciHfXWXrUWY8HRLh7hO7.UPRETSfjFY8HBb3HBH1EFa0UVOhDiHu3COPEjTA0DHoQVOh.WNh.hcgwVck0iHwHxK9vyKSAUQXgkO.bUUtslaucma.f..Y.fI.rB.3..P.fD.MAvW.PF.oE.LATS.2DPNAvS.9D.QAbT.NEvTATU.ZQ.1........BD..........X...................D.N"
						}
,
						"snapshotlist" : 						{
							"current_snapshot" : 0,
							"entries" : [ 								{
									"filetype" : "C74Snapshot",
									"version" : 2,
									"minorversion" : 0,
									"name" : "Venom",
									"origin" : "Venom.auinfo",
									"type" : "AudioUnit",
									"subtype" : "AudioEffect",
									"embed" : 0,
									"snapshot" : 									{
										"pluginname" : "Venom.auinfo",
										"plugindisplayname" : "Venom",
										"pluginsavedname" : "C74_AU:/Venom",
										"pluginsaveduniqueid" : 1449487983,
										"version" : 1,
										"isbank" : 0,
										"isbase64" : 1,
										"sliderorder" : [  ],
										"slidervisibility" : [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
										"blob" : "1328.hAGaoMGcv.C1AHv.DTfAGfPBJrvDTTgEWvUag4VclE1XzUmbkIGUjEFcgwUYrUVak4Fcs3VXsU1UyUmXzkGbkckckI2bo8laTQWdvU1WP7fZ0MVYPwVcmklaSQWXzUFUtEVakIwUgAmbOAAw..............vE..PCA+C......zfv........ML7Oa0ls..PCDC.......zPw+.......MXL.......PCGC.......z.x+.H.....MjL......DfpO9Cf....AnJj+.....P.pF4O.B...DfpR9C.....An5j+.H...P.pR4O.....DfpU9C.....Anpk+.H...P.pdoO.B...Dfpt9SFuEG.An5q+jwawAP.pBK......Dfpw5Cf....Anpr9vLyMKMCM3PDQESTxD8CPDELUkjavUGcQ+fDV8TczAWczIgUk41aP.fDgUmY38TDCnmUCISHwM...vyTPUDVXARcyU1QL0iHvHBHsUGazkFcnIWYgQVZtcVOh.iHfLFZgkla8HBQA0DTI4zQrPTQCETVrXTQAoUQrXzSCU0TrzTRRI0SRwBTIQ0PHwxTL8DTEIBHvIWYyUFcNEVak0iHDUlYgUGazIBHyUFakMFckQVQlYVYiQWOhHhO7.UPRETSfjFY8HBbwHBH1EFa0UVOhDiKvbyL0TCLvLyL0XSNyLiMkEiHu3COPEjTA0DHoQVOh.WLvHBH1EFa0UVOhDiHu3COPEjTA0DHoQVOh.WLwHBH1EFa0UVOhbiK1biM4fCM3XyLxfSLxTSYxHxK9vCTAIUPMARZj0iHvEiLh.hcgwVck0iHwHxK9vCTAIUPMARZj0iHvEyLh.hcgwVck0iHx3xLzPCLv.yLyjSMvfCL0bSYsDiHu3COPEjTA0DHoQVOh.WLzHBH1EFa0UVOh.iHu3COPEjTA0DHoQVOh.WL0HBH1EFa0UVOhbiK2LCM4jSN1TiM1byMxPiMk0RLh7hO7.UPRETSfjFY8HBbwXiHfXWXrUWY8HBMtPiMvfCNxfyMyTyL0DSM1TlLh7hO7.UPRETSfjFY8HBbwbiHfXWXrUWY8HBLh7hO7.UPRETSfjFY8HBbwfiHfXWXrUWY8HBNtDSNv.CLv.SM2HiLvPSM4TVKwHxK9vCTAIUPMARZj0iHvIiHfXWXrUWY8HBLh7hO7.UPRETSfjFY8HBbx.iHfXWXrUWY8HRKyHxK9vCTAIUPMARZj0iHvISLh.hcgwVck0iHsLiHu3COPEjTA0DHoQVOh.mLxHBH1EFa0UVOh.iHu3COPEjTA0DHoQVOh.mLyHBH1EFa0UVOhLiHu3COPEjTA0DHoQVOh.mLzHBH1EFa0UVOhHiHu3COPEjTA0DHoQVOh.2Lh.hcgwVck0iH33RN4jSN4jyM1DSM3DCMxDSYsDiHu3COPEjTA0DHoQVOh.GMh.hcgwVck0iHvHxK9vCTAIUPMARZj0iHvUiHfXWXrUWY8HxLkIiHu3COPEjTA0DHoQVOh.mMh.hcgwVck0iHvHxK9vCTAIUPMARZj0iHvciHfXWXrUWY8HRLh7hO7.UPRETSfjFY8HBb3HBH1EFa0UVOhDiHu3COPEjTA0DHoQVOh.WNh.hcgwVck0iHwHxK9vyKSAUQXgkO.bUUtslaucma.f..Y.fI.rB.3..P.fD.MAvW.PF.oE.LATS.2DPNAvS.9D.QAbT.NEvTATU.ZQ.1........BD..........X...................D.N"
									}
,
									"fileref" : 									{
										"name" : "Venom",
										"filename" : "Venom.maxsnap",
										"filepath" : "~/Documents/Max 8/Snapshots",
										"filepos" : -1,
										"snapshotfileid" : "15e03d29725ead6075742e8e06a51574"
									}

								}
 ]
						}

					}
,
					"text" : "vst~ C74_AU:/Venom",
					"varname" : "vst~[1]",
					"viewvisibility" : 1
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-7",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 503.0, 340.0, 384.0, 22.0 ],
					"text" : "bang"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-33",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 358.0, 100.0, 83.0, 22.0 ],
					"text" : "vexpr $f1 * 10"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-32",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 376.0, 166.0, 97.0, 22.0 ],
					"text" : "prepend position"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-28",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 491.0, 76.0, 177.0, 22.0 ],
					"text" : "vexpr ($f1 * (-360) / (3.141593))"
				}

			}
, 			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 13.0,
					"id" : "obj-23",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 491.0, 124.0, 113.0, 23.0 ],
					"text" : "prepend rotatexyz"
				}

			}
, 			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 13.0,
					"id" : "obj-31",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "jit_matrix", "" ],
					"patching_rect" : [ 491.0, 209.0, 285.0, 23.0 ],
					"text" : "jit.gl.gridshape euler-ctx @shape cube @axes 1"
				}

			}
, 			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 13.0,
					"frozen_object_attributes" : 					{
						"rect" : [ 695, 45, 1015, 285 ]
					}
,
					"id" : "obj-42",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "bang", "" ],
					"patching_rect" : [ 795.0, 188.0, 124.0, 23.0 ],
					"text" : "jit.window euler-ctx"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-29",
					"maxclass" : "toggle",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "int" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 706.0, 50.5, 24.0, 24.0 ]
				}

			}
, 			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 13.0,
					"id" : "obj-27",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"patching_rect" : [ 706.0, 78.5, 76.0, 23.0 ],
					"text" : "qmetro 20"
				}

			}
, 			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 13.0,
					"id" : "obj-26",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "bang", "erase" ],
					"patching_rect" : [ 706.0, 107.5, 63.0, 23.0 ],
					"text" : "t b erase"
				}

			}
, 			{
				"box" : 				{
					"fontname" : "Arial",
					"fontsize" : 13.0,
					"id" : "obj-24",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "bang", "" ],
					"patching_rect" : [ 706.0, 142.5, 219.0, 23.0 ],
					"text" : "jit.gl.render euler-ctx @camera 0 0 8"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-21",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 32.0, 329.0, 78.0, 20.0 ],
					"text" : "Rotation"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-20",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 32.0, 241.0, 78.0, 20.0 ],
					"text" : "Translation"
				}

			}
, 			{
				"box" : 				{
					"format" : 6,
					"id" : "obj-17",
					"maxclass" : "flonum",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 214.0, 330.0, 81.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"format" : 6,
					"id" : "obj-18",
					"maxclass" : "flonum",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 304.0, 330.0, 81.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"format" : 6,
					"id" : "obj-19",
					"maxclass" : "flonum",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 126.0, 330.0, 81.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-15",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "float", "float", "float" ],
					"patching_rect" : [ 138.0, 125.0, 87.0, 22.0 ],
					"text" : "unpack 0. 0. 0."
				}

			}
, 			{
				"box" : 				{
					"format" : 6,
					"id" : "obj-14",
					"maxclass" : "flonum",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 214.0, 241.0, 81.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"format" : 6,
					"id" : "obj-13",
					"maxclass" : "flonum",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 304.0, 241.0, 81.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"format" : 6,
					"id" : "obj-11",
					"maxclass" : "flonum",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 126.0, 241.0, 81.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-8",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "float", "float", "float" ],
					"patching_rect" : [ 32.0, 125.0, 87.0, 22.0 ],
					"text" : "unpack 0. 0. 0."
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-3",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 4,
					"outlettype" : [ "", "", "", "" ],
					"patching_rect" : [ 32.0, 59.0, 221.0, 22.0 ],
					"text" : "OSC-route /translation /rotation /classes"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-1",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 32.0, 35.0, 97.0, 22.0 ],
					"text" : "udpreceive 8888"
				}

			}
 ],
		"lines" : [ 			{
				"patchline" : 				{
					"destination" : [ "obj-3", 0 ],
					"source" : [ "obj-1", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-39", 1 ],
					"source" : [ "obj-10", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-39", 0 ],
					"source" : [ "obj-10", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-17", 0 ],
					"order" : 1,
					"source" : [ "obj-15", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-18", 0 ],
					"source" : [ "obj-15", 2 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-19", 0 ],
					"order" : 1,
					"source" : [ "obj-15", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-34", 0 ],
					"order" : 0,
					"source" : [ "obj-15", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-41", 0 ],
					"order" : 0,
					"source" : [ "obj-15", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 0 ],
					"source" : [ "obj-16", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-31", 0 ],
					"source" : [ "obj-23", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-24", 0 ],
					"source" : [ "obj-26", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-24", 0 ],
					"source" : [ "obj-26", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-26", 0 ],
					"source" : [ "obj-27", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-23", 0 ],
					"source" : [ "obj-28", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-27", 0 ],
					"source" : [ "obj-29", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-15", 0 ],
					"order" : 1,
					"source" : [ "obj-3", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-28", 0 ],
					"order" : 0,
					"source" : [ "obj-3", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-33", 0 ],
					"order" : 0,
					"source" : [ "obj-3", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-7", 1 ],
					"source" : [ "obj-3", 2 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-8", 0 ],
					"order" : 1,
					"source" : [ "obj-3", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-31", 0 ],
					"source" : [ "obj-32", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-32", 0 ],
					"source" : [ "obj-33", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-16", 0 ],
					"source" : [ "obj-34", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 0 ],
					"source" : [ "obj-40", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-40", 0 ],
					"source" : [ "obj-41", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 1 ],
					"source" : [ "obj-44", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 0 ],
					"source" : [ "obj-44", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-11", 0 ],
					"source" : [ "obj-8", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-13", 0 ],
					"source" : [ "obj-8", 2 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-14", 0 ],
					"source" : [ "obj-8", 1 ]
				}

			}
 ],
		"parameters" : 		{
			"obj-10" : [ "vst~[1]", "vst~[1]", 0 ],
			"parameterbanks" : 			{

			}
,
			"inherited_shortname" : 1
		}
,
		"dependency_cache" : [ 			{
				"name" : "Venom.maxsnap",
				"bootpath" : "~/Documents/Max 8/Snapshots",
				"patcherrelativepath" : "../../../../Documents/Max 8/Snapshots",
				"type" : "mx@s",
				"implicit" : 1
			}
, 			{
				"name" : "11_vc_kontaktstelle4.wav",
				"bootpath" : "~/devel/MagicQueen/vcstereo",
				"patcherrelativepath" : "../../vcstereo",
				"type" : "WAVE",
				"implicit" : 1
			}
, 			{
				"name" : "OSC-route.mxo",
				"type" : "iLaX"
			}
 ],
		"autosave" : 0
	}

}
