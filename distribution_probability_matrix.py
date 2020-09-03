#!/bin/env python
import os

class ParseFile():
    """

    """
    def __init__(self, file_path):
        self.path_name = file_path
        self.info_name = os.path.basename(file_path)
        self.offset = -1
        self.value  = -1
        self.bitmap = {}
        self._get_probe_info()
        self._parse_file()

    def _get_probe_info(self):
        info_list = self.info_name.split("-")
        if(len(info_list) == 2):
            self.type = "orig"
            self.name = info_list[0]
        else:
            self.name = info_list[0]
            self.offset    = int(info_list[1])
            self.value     = int(info_list[2],16)
            self.type = "data"

    def _parse_file(self):
        with open (self.path_name,"r") as f:
            for line in f.readlines:
                bitmap_id    = line.split(":")[0]
                bitmap_times = line.split(":")[1]
                self.bitmap.update({bitmap_id : bitmap_times})


class CollectMatrix():

    def __init__(self,input_dir):
        self.total_bitmap_info = {}
        self.total_coverage_similarity_matrix = {}
        self.total_frequency_difference_matrix = {}
        self.inputs_path = input_dir

    def start_work(self):

        self._get_info_file_to_dict()
        print "parse finish"
        print ""
        self._handle_info_dict()
        print "dict finish"
        self._print_info_matrix()

    def _update_total_bitmap_info(self):

        input_name   = self.info.name
        buf_offset   = self.info.offset
        buf_value    = self.info.value
        input_type   = self.info.type
        bitmap       = self.info.bitmap

        if (self.total_bitmap_info.has_key(input_name)):
            if(input_type == "orig"):
                self.total_bitmap_info.update({input_name:{"orig":bitmap}})
            else:
                if(self.total_bitmap_info[input_name].has_key(buf_offset)):
                    self.total_bitmap_info[input_name][buf_offset].update({buf_value:bitmap})
                else:
                    self.total_bitmap_info[input_name].update({buf_offset:{buf_value:bitmap}})

        else:
            if(input_type == "orig"):
                self.total_bitmap_info.update({input_name:{"orig":bitmap}})
            else:
                self.total_bitmap_info.update({input_name:{{buf_offset:{buf_value:bitmap}}}}) 

    def _get_info_file_to_dict(self):

        for info_file_path in self.inputs_path:
            self.info = ParseFile(info_file_path)
            self.update_total_bitmap_info()
        print "a"

    def _get_coverage_simalarity(self, orig, new):

        merge = orig.copy()
        merge.update(new)
        union = len(merge)
        intersection_num = 0
        for bitmap_id in merge.keys():
            if orig.hes_key(bitmap):
                intersection_num += 1

        return intersection/union

    def _get_frequency_difference(self, orig, new):

        merge = orig.copy()
        merge.update(new)
        intersection_index = []
        new_inter_index = []
        orig_inter_index = []
        differ_frequence = 0
        differ_coverage = 0

        for bitmap_id in merge.keys():
            if orig.has_key(bitmap):
                intersection_index.append(bitmap_id)
            else:
                new_inter_index.append(bitmap_id)
            if not new.has_key(bitmap): 
                orig_inter_index.append(bitmap_id)

        for bit_map_id in inter_index:
            if (orig[bit_map] == orig[bit_map]):
                continue
            differ_frequence +=1

        for bit_map_id in new_inter_index:
            if (orig[bit_map] == orig[bit_map]):
                continue
            differ_coverage +=1

        for bit_map_id in new_inter_index:
            if (orig[bit_map] == orig[bit_map]):
                continue
            differ_coverage +=1
        return differ_frequence/differ_coverage



    def _handle_info_dict(self):

        for input_name in self.total_bitmap_info.keys():
            orig_bitmap = self.total_bitmap_info[input_name]["orig"]
            offset_cov_dict  = {}
            offset_freq_dict = {}
            for offset in self.total_bitmap_info[input_name].keys():
                if (offset == "orig"):
                    continue
                cov_sim_dict   = {}
                freq_diff_dict = {}
                for value in self.total_bitmap_info[input_name][offset].keys():
                    changed_bitmap = self.total_bitmap_info[input_name][offset][value]
                    cov_sim   = _get_coverage_simalarity(self, orig_bitmap, changed_bitmap)
                    freq_diff = _get_frequency_difference(self, orig_bitmap, changed_bitmap)
                    cov_sim_dict.update({value:cov_sim})
                    freq_diff_dict.update({value:freq_diff})
                offset_cov_dict.update({offset:cov_sim_dict})
                offset_freq_dict.update({offset:freq_diff_dict})
            self.total_coverage_similarity_matrix.update({input_name:offset_cov_dict})
            self.total_frequency_difference_matrix.update({input_name:offset_freq_dict})

    def _print_info_matrix(self):
        with open ("matix_outi_cov_sim.data","rw+")as f:
            for file_name in self.total_coverage_similarity_matrix.keys():
                f.writelines(file_name)
                for buf_offset in total_coverage_similarity_matrix[file_path].keys():
                    cov_sim_info_dict = total_coverage_similarity_matrix[file_path][buf_offset]
                    changed_value = cov_sim_info_dict.keys()
                    for i in changed_value:
                        f.write(i)
                        f.write(",")
                    f.write("\n")
                    for i in changed_value:
                        f.write(cov_sim_info_dict[i])
                        f.write(",")
                    f.write("\n")

        with open ("matix_outi_freq_dif.data","rw+")as f:
            for file_name in self.total_frequency_difference_matrix.keys():
                f.writelines(file_name)
                for buf_offset in total_frequency_difference_matrix[file_path].keys():
                    freq_dif_info_dict = total_frequency_difference_matrix[file_path][buf_offset]
                    changed_value = freq_dif_info_dict.keys()
            for i in changed_value:
                f.write(i)
                f.write(",")
            f.write("\n")
            for i in changed_value:
                f.write(freq_dif_info_dict[i])
                f.write(",")
            f.write("\n")





def main():
    """"""
    bitmap_file_dir="/tmp/lhy/probe/probe"
    a = CollectMatrix(bitmap_file_dir)
    a.start_work()


if __name__ == "__main__":
    main()
