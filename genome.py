### genome.py



class Genome():

    def __init__(self,
                 genome_input_dtypes, genome_output_dtypes,
                 genome_main_count, genome_arg_count):

        # Genome - Argument List
        self.args_count = genome_arg_count
        self.args = [None]*genome_arg_count
        self.arg_methods = [None]
        self.arg_weights = [None]

        # Genome - Ftn List
        self.genome = [None]*(len(genome_inputs_dtypes)+genome_main_count+len(genome_output_dtypes))
        self.genome_count = len(self.genome)

        # Block - Genome List - Input Nodes
        self.genome_input_dtypes = genome_input_dtypes # a list of data types. the exact values will be assigned at evaluation step
        self.genome_input_count = len(genome_input_dtypes)
        self.genome[-1*len(genome_input_dtypes):] = ["InputPlaceholder"]*len(genome_input_dtypes)#block_inputs

        # Block - Genome List - Main Nodes
        self.genome_main_count = genome_main_count
        self.ftn_methods = [None]
        self.ftn_weights = [None]

        # Block - Genome List - Outputs Nodes
        self.genome_output_dtypes = genome_output_dtypes # a list of data types. the exact values will be evaluated at evaluation step
        self.genome_output_count = len(genome_output_dtypes)


    def __setitem__(self, node_index, dict_):
        self.genome[node_index] = dict_


    def __getitem__(self, node_index):
        return self.genome[node_index]


    def buildWeights(self, method, method_dict):
        prob_remaining = 1.0
        weights = [0] * len(method_dict)
        equally_distribute = []
        for i, m in enumerate(self.__dict__[method]):
            if method_dict[m]['prob'] <= 0:
                # will never call this method
                # setting weight to 0 instead of removing
                # ...my guess is that it's more useful to see that it's set to 0 rather than gone
                pass
            elif method_dict[m]['prob'] < 1:
                # assign it that prob
                prob_remaining -= method_dict[m]['prob']
                if prob_remaining < 0:
                    # error, sum of prob is greater than 1
                    print("UserInputError: current sum of prob/weights for %s is > 1" % method)
                    exit()
                else:
                    weights[i] = method_dict[m]['prob']
            else:
                # user wants this prob to be equally distributed with whatever is left
                equally_distribute.append(i)
        # we looped through all methods, now equally distribute the remaining amount
        if len(equally_distribute) > 0:
            eq_weight = round(prob_remaining/len(equally_distribute), 4)
            for i in equally_distribute:
                weights[i] = eq_weight
        else:
            pass
        # now clean up any rounding errors by appending any remainder to the last method
        remainder = 1 - sum(weights)
        if remainder > .01:
            print("UserInputError: total sum of prob/weights for %s is < .99" % method)
            exit()
        else:
            weights[-1] += remainder
        return weights


    def getNodeType(self, node_index, arg_dtype=False, input_dtype=False, output_dtype=False):
        if node_index < 0:
            # then it's a Block Input Node
            return self.block_inputs_dtypes[-1*node_index-1] # -1-->0, -2-->1, -3-->2
        elif node_index >= self.block_main_count:
            # then it's a Block Output Node
            return self.block_outputs_dtypes[node_index-self.block_main_count]
        else:
            # then it's a Block Main Node
            pass 
        ftn = self[node_index]["fnt"]
        ftn_dict = operator_dict[ftn]
        if input_dtype:
            # get the required input data types for this function
            return ftn_dict["inputs"] # will return a list
        elif output_dtype:
            # get the output data types for this function
            return ftn_dict["outputs"] # returns a single value, not a list...arity is always 1 for outputs
        elif arg_dtype:
            return ftn_dict["args"]
        else:
            print("ProgrammerError: script writer didn't assign input/output dtype for getNodeType method")
            exit()


    def randomFtn(self, only_one=False, exclude=None):
        choices = self.ftn_methods
        weights = self.ftn_weights
        if exclude is not None:
            for val in exclude:
                choices = np.delete(choices, np.where(choices==val))
                weights = np.delete(weights, np.where(choices==val))
        else:
            pass
        if only_one:
            return np.random.choice(a=choices, size=1, p=weights)
        else:
            return np.random.choice(a=choices, size=len(self.ftn_methods), replace=False, p=weights)


    def randomInput(self, dtype, min_=-1*self.block_inputs_count, max_=self.block_main_count, exclude=None):
        # max_ is one above the largest integer to be drawn
        # so if we are randomly finding nodes prior to a given node index, set max_ to that index
        choices = np.arange(min_, max_)
        if exclude is not None:
            for val in exclude:
                choices = np.delete(choices, np.where(choices==val))
        else:
            pass
        possible_nodes = np.random.choice(a=choices, size=max_-min_, replace=False)
        # iterate through each input until we find a datatype that matches dtype
        for poss_node in possible_nodes:
            poss_node_outputdtype = self.getNodeType(node_index=poss_node, output_dtype=True)
            # note, we currently only allow for arity of 1 for our ftns...so getNodeType will return a value not a list if output_dtype is True
            if dtype == poss_node_outputdtype:
                return poss_node
            else:
                pass
        # if we got this far then we didn't find a match
        return None


    def randomArg(self, dtype, exclude=None):
        choices = []
        for arg_index in range(self.args_count):
            if arg_index in exclude:
                continue
            else:
                pass
            arg_dtype = type(self.args[arg_index]).__name__
            if dtpye == arg_dtype:
                choices.append(arg_index)
        if len(choices) == 0:
            print("UserInputError: A ftn was provided without having its required data type in the arguments")
            exit()
        else:
            return np.random.choice(a=choices, size=1)


    def fillArgs(self):
        start_point = 0
        end_point = 0
        for arg_index, arg_class in enumerate(self.arg_methods):
            end_point += round(self.arg_weights[arg_index]*self.genome_arg_count)
            self.args[start_point:end_point] = arg_class() # need some way to initialize the args here...call mutate?
            start_point = end_point
        if end_point != self.genome_arg_count:
            # some wierd rounding error then...just go ahead and asign the last few with the previous batch
            self.args[end_point:self.genome_arg_count] = arg_class() # ...use method from above
        else:
            pass


    def fillGenome(self, operator_dict)
        # Genome - Main Nodes
        for node_index in range(self.genome_main_count):
            # randomly select all function, find a previous node with matching output_dtype matching our function input_dtype
            # iterate through each function until you find matching output and input data types
            ftns = self.randomFtn()
            for ftn in ftns:
                # connect to a previous node
                input_dtypes = operator_dict[ftn]["inputs"]
                input_nodes = [] # [None]*len(input_dtypes)
                for input_dtype in input_dtypes:
                    input_nodes.append(self.randomInput(max_=node_index, dtype=input_dtype))
                if None in input_nodes:
                    # couldn't find a matching input + output value. try the next ftn
                    break
                else:
                    # go on to find args
                    pass
                # connect to any required arguments
                arg_dtypes = operator_dict[ftn]["args"]
                arg_nodes = []
                for arg_dtype in arg_dtypes:
                    arg_nodes.append(self.randomArg(dtype=arg_dtype))
                # assign all values to the genome
                self.genome[node_index] = {"ftn": ftn,
                                           "inputs": input_nodes,
                                           "args": arg_nodes}
                # we found a ftn that works, move on to next node_index
                break
        # Genome - Output Nodes
        for i, output_dtype in enumerate(self.genome_output_dtypes):
            self.genome[genome_main_count+i] = self.randomInput(min_=0, max_=self.genome_main_count, dtype=output_dtype)


    def findActive(self):
        """
        Acitve nodes should include:
        * all OUTPUT nodes
        * any INPUT node eventually connected to output (expressed as negative positions: -1, -2, etc)
        * any MAIN node eventually connected to output
        """
        self.active_nodes = set(range(self.block_main_count, self.block_main_count+self.block_outputs_count))
        self.active_ftns = set() #not sure what the point is here
        self.active_args = set()
        # update with which nodes feed into the block outputs
        for node_input in self.active_nodes:
            self.active_nodes.update(self[node_index])
        # update what feed into the block main nodes
        for node_index in reversed(range(self.block_main_count)):
            if node_index in self.active_nodes:
                # check which nodes are input to this node_index...then update our active_nodes set list
                self.active_nodes.update(self[node_index]["inputs"])
                self.active_ftns.update([self[node_index]["ftn"]])
                if len(self[node_index]["args"]) > 0:
                    self.active_args.update(self[node_index]["args"])
                else: # no args to update
                    pass
                if (not self.has_learner) and (self[node_index]["ftn"].__name__=="single_learner"):
                    self.has_learner = True
                else: # already learned or ftn isn't a learner
                    pass
            else: # not an active node; don't care
                pass
        self.active_nodes = sorted(list(self.active_nodes))
        self.active_ftns = sorted(list(self.active_ftns))
        self.active_args = sorted(list(self.active_args))