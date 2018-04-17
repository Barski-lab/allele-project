import copy
import subprocess
import sys

class TYPE:
    INS = 1,
    DEL = 2


class RefInterval:

    def __init__(self):
        self.reset()

    def reset(self):
        self.chrom = None
        self.pose = [0, 0]
        self.old_shift = 0
        self.shift = 0
        self.next_shift = 0
        self.type = None

    def move(self, ref_line):
        ref_list = ref_line.strip().split('\t')
        if self.chrom != ref_list[0]: self.reset()
        self.chrom = ref_list[0]
        self.pose[0] = self.pose[1]
        self.pose[1] = int(ref_list[1])
        self.old_shift = self.shift
        self.shift = self.next_shift
        self.type = (self.shift > self.old_shift and TYPE.INS) or (self.shift < self.old_shift and TYPE.DEL) or None
        self.next_shift = int(ref_list[2])

    def includes(self, chrom, position):
        return chrom == self.chrom and self.pose[0] <= position < self.pose[1]

    def on_del_start(self, position):
        return position == self.pose[0] and self.type == TYPE.DEL

    def __str__ (self):
        return "Chrom: {}\t Pose: {}\t Old shift: {}\t Shift: {}\t Next shift: {}\t Type: {}\n"\
            .format(self.chrom, self.pose, self.old_shift, self.shift, self.next_shift, self.type)


class BedInterval:

    def __init__(self, bed_line="''\t0\t0\t0"):
        bed_list = bed_line.strip().split('\t')
        self.chrom = bed_list[0]
        self.pose = [int(bed_list[1]), int(bed_list[2])]
        self.value = float(bed_list[3])

    def shift (self, idx, shift_value):
        self.pose[idx] += shift_value

    def __str__ (self):
        return "{}\t{}\t{}\t{}\n".format(self.chrom, self.pose[0], self.pose[1], self.value)


class IntervalProjector:

    ref_pointer = 0

    def __init__(self, ref_path, bed_path, output_path):
        self.ref_file = ref_path
        self.bed_file = bed_path
        self.output_file = output_path
        self.ref_interval = RefInterval()
        self.ref_interval_backup = RefInterval()
        self.bed_wc_l = 1
        self.preliminary_check()

    def preliminary_check(self):
        """Checks if chromosomes order is identical between BED and REF files. Raise if smth is not correct"""
        ref_output = subprocess.check_output("cat {} | cut -f 1 | sort -u".format(self.ref_file), shell=True)
        bed_output = subprocess.check_output("cat {} | cut -f 1 | sort -u".format(self.bed_file), shell=True)
        self.bed_wc_l = subprocess.check_output("cat {} | wc -l".format(self.bed_file), shell=True)
        if ref_output != bed_output:
            print "Chromosome list or order is different"
            print "BED\n", bed_output
            print "REF\n", ref_output
            raise Exception

    def reset_data(self):
        self.ref_interval.reset()
        self.ref_interval_backup.reset()

    def restore_ref_interval(self, file_stream):
        file_stream.seek(self.ref_pointer)
        self.ref_interval = copy.deepcopy(self.ref_interval_backup)

    def backup_ref_interval(self, file_stream):
        self.ref_pointer = file_stream.tell()
        self.ref_interval_backup = copy.deepcopy(self.ref_interval)

    def print_progress(self, cur_line):
        step = round (float(self.bed_wc_l)/float(5))
        if cur_line%step == 0:
            print round(float(cur_line)/float(self.bed_wc_l)*100)

    def project(self):
        with open(self.ref_file, 'r') as ref_stream, open(self.bed_file, 'r') as bed_stream, open(self.output_file,'w') as output_stream:
            for cur_line, bed_line in enumerate(bed_stream, start=1):
                self.print_progress(cur_line)
                bed_interval = BedInterval(bed_line)
                self.restore_ref_interval(ref_stream)
                for idx, position in enumerate(bed_interval.pose):
                    ref_line = True
                    while ref_line:
                        if self.ref_interval.includes(bed_interval.chrom, position):
                            shift = -self.ref_interval.old_shift if idx == 1 and self.ref_interval.on_del_start(position) else -self.ref_interval.shift
                            bed_interval.shift(idx, shift)
                            break
                        if idx == 0: self.backup_ref_interval(ref_stream)
                        ref_line = ref_stream.readline()
                        if ref_line: self.ref_interval.move(ref_line)
                output_stream.write(str(bed_interval))


