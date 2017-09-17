source = [	'videos/bus/bus000.avi',
		    'videos/bus/bus001.avi',
		    'videos/bus/bus010.avi',
		    'videos/bus/bus011.avi',
		    'videos/bus/bus100.avi',
		    'videos/bus/bus101.avi',
		    'videos/bus/bus110.avi',
		    'videos/bus/bus111.avi',
		    'videos/bus/bus120.avi',
		    'videos/bus/bus121.avi', ]
destination_ratio = [ 0.1, 0.2, 0.3 ]
noise_ratio = dict(zip(destination_ratio, [ 0.2, 0.4, 0.6 ]))
noise_type = [ 1, 2 ]
noise_value = dict(zip(noise_type, [[ 64000, 128000, 256000 ], [ 1024000, 4096000, 8192000 ]]))

file_object=open("application_test_cases.txt",'w')

for i in source:
	for j in destination_ratio:
		for k in noise_type:
			for l in noise_value[k]:
				line=(	"'"+str(i)+"' "+
						"'"+str(j)+"' "+
						"'' "+
						"'' "+
						"'"+str(noise_ratio[j])+"' "+
						"'"+str(k)+"' "+
						"'' "+
						"'"+str(l)+"' "+
						"'' "+
						"''")
				file_object.write(line+"\n")

file_object.close()
