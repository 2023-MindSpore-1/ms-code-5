# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 14:34:25 2020

@author: zjs
"""
import Loss
import torch
import numpy as np
import random as rd
import torch.nn as nn
import torch.nn.functional as F

import mindspore as ms
from mindspore import nn
from mindspore.common.initializer import initializer, Uniform, XavierUniform, One


#class model(nn.Module):
class model(nn.Cell):
    
    def __init__(self, numOfEntity, numOfRelation, numOfhidden, dataset, ns):
        super(model,self).__init__()
        self.numOfEntity = numOfEntity
        self.numOfRelation = numOfRelation
        self.numOfhidden = numOfhidden
        self.dataset = dataset
        self.norm = 2
        self.ns = ns
        self.prob = 0.0
        self.numOfCommunity = 6
        
        sqrtR = numOfhidden**0.5
        sqrtE = numOfhidden**0.5

        # self.relation_embeddings = nn.Embedding(self.numOfRelation+1, self.numOfhidden, padding_idx=self.numOfRelation)
        # #nn.init.xavier_uniform_(self.relation_embeddings.weight[0:self.numOfRelation])
        # self.relation_embeddings.weight.data[0:self.numOfRelation] = torch.FloatTensor(self.numOfRelation, self.numOfhidden).uniform_(-1./sqrtR, 1./sqrtR)
        # self.relation_embeddings.weight.data[0:self.numOfRelation] = F.normalize(self.relation_embeddings.weight.data[0:self.numOfRelation], 2, 1)

        self.relation_embeddings = ms.nn.Embedding(self.numOfRelation + 1, self.numOfhidden,
                                                padding_idx=self.numOfRelation)
        # nn.init.xavier_uniform_(self.relation_embeddings.weight[0:self.numOfRelation])
        self.relation_embeddings.embedding_table.data[0:self.numOfRelation] = ms.Tensor(shape=(self.numOfRelation, self.numOfhidden),
                                                                                           dtype=ms.float32, init=Uniform(scale=1. / sqrtR))
        self.relation_embeddings.embedding_table.data[0:self.numOfRelation] = ms.ops.L2Normalize(axis=1, epsilon=1e-12)\
            (self.relation_embeddings.embedding_table.data[0:self.numOfRelation])

        # self.entity_embeddings_y1 = nn.Embedding(self.numOfEntity + 1, 30, padding_idx=self.numOfEntity)
        # nn.init.xavier_uniform_(self.entity_embeddings_y1.weight[0:self.numOfEntity])
        self.entity_embeddings_y1 = ms.nn.Embedding(self.numOfEntity+1, 30, padding_idx=self.numOfEntity)
        self.entity_embeddings_y1.embedding_table.data[0:self.numOfEntity] = initializer(XavierUniform(),
                                                                           self.entity_embeddings_y1.embedding_table[0:self.numOfEntity].shape)

        # self.entity_embeddings_m1 = nn.Embedding(self.numOfEntity + 1, 30, padding_idx=self.numOfEntity)
        # nn.init.xavier_uniform_(self.entity_embeddings_m1.weight[0:self.numOfEntity])
        self.entity_embeddings_m1 = ms.nn.Embedding(self.numOfEntity+1, 30, padding_idx=self.numOfEntity)
        self.entity_embeddings_m1.embedding_table.data[0:self.numOfEntity] = initializer(XavierUniform(),
                                                                           self.entity_embeddings_m1.embedding_table[0:self.numOfEntity].shape)

        # self.entity_embeddings_d1 = nn.Embedding(self.numOfEntity + 1, 40, padding_idx=self.numOfEntity)
        # nn.init.xavier_uniform_(self.entity_embeddings_d1.weight[0:self.numOfEntity])
        self.entity_embeddings_d1 = ms.nn.Embedding(self.numOfEntity+1, 40, padding_idx=self.numOfEntity)
        self.entity_embeddings_d1.embedding_table.data[0:self.numOfEntity] = initializer(XavierUniform(),
                                                                           self.entity_embeddings_d1.embedding_table[0:self.numOfEntity].shape)

        # self.entity_embeddings_y2 = nn.Embedding(self.numOfEntity + 1, 30, padding_idx=self.numOfEntity)
        # nn.init.xavier_uniform_(self.entity_embeddings_y2.weight[0:self.numOfEntity])
        self.entity_embeddings_y2 = ms.nn.Embedding(self.numOfEntity+1, 30, padding_idx=self.numOfEntity)
        self.entity_embeddings_y2.embedding_table.data[0:self.numOfEntity] = initializer(XavierUniform(),
                                                                           self.entity_embeddings_y2.embedding_table[0:self.numOfEntity].shape)

        # self.entity_embeddings_m2 = nn.Embedding(self.numOfEntity + 1, 30, padding_idx=self.numOfEntity)
        # nn.init.xavier_uniform_(self.entity_embeddings_m2.weight[0:self.numOfEntity])
        self.entity_embeddings_m2 = ms.nn.Embedding(self.numOfEntity+1, 30, padding_idx=self.numOfEntity)
        self.entity_embeddings_m2.embedding_table.data[0:self.numOfEntity] = initializer(XavierUniform(),
                                                                           self.entity_embeddings_m2.embedding_table[0:self.numOfEntity].shape)

        # self.entity_embeddings_d2 = nn.Embedding(self.numOfEntity + 1, 40, padding_idx=self.numOfEntity)
        # nn.init.xavier_uniform_(self.entity_embeddings_d2.weight[0:self.numOfEntity])
        self.entity_embeddings_d2 = ms.nn.Embedding(self.numOfEntity+1, 40, padding_idx=self.numOfEntity)
        self.entity_embeddings_d2.embedding_table.data[0:self.numOfEntity] = initializer(XavierUniform(),
                                                                           self.entity_embeddings_d2.embedding_table[0:self.numOfEntity].shape)


        # self.entity_embeddings_v3 = nn.Embedding(self.numOfEntity+1, self.numOfhidden, padding_idx=self.numOfEntity)
        # #nn.init.xavier_uniform_(self.entity_embeddings_v3.weight[0:self.numOfEntity])
        # self.entity_embeddings_v3.weight.data[0:self.numOfEntity] = torch.FloatTensor(self.numOfEntity, self.numOfhidden).uniform_(-1./sqrtE, 1./sqrtE)
        # self.entity_embeddings_v3.weight.data[0:self.numOfEntity] = F.normalize(self.entity_embeddings_v3.weight.data[0:self.numOfEntity], 2, 1)
        self.entity_embeddings_v3 = ms.nn.Embedding(self.numOfEntity+1, self.numOfhidden, padding_idx=self.numOfEntity)
        #nn.init.xavier_uniform_(self.entity_embeddings_v3.weight[0:self.numOfEntity])
        self.entity_embeddings_v3.embedding_table.data[0:self.numOfEntity] = ms.Tensor(shape=(self.numOfEntity, self.numOfhidden),
                                                                                          dtype=ms.float32, init=Uniform(1./sqrtE))
        self.entity_embeddings_v3.embedding_table.data[0:self.numOfEntity] = ms.ops.L2Normalize(axis=1, epsilon=1e-12)\
            (self.entity_embeddings_v3.embedding_table.data[0:self.numOfEntity])

        # self.Transfer_R = nn.Linear(self.numOfhidden, self.numOfhidden, bias=False)
        # self.Transfer_E = nn.Linear(self.numOfhidden, self.numOfhidden, bias=False)
        self.Transfer_R = ms.nn.Dense(self.numOfhidden, self.numOfhidden, has_bias=False)
        self.Transfer_E = ms.nn.Dense(self.numOfhidden, self.numOfhidden, has_bias=False)
        if "forecast" in self.dataset:
            # self.decay_rate = torch.nn.Parameter(data=torch.cuda.FloatTensor([[0.00]]),
            #                                      requires_grad=False)  # ICEWS18, 05, 0 requires_grad = False
            self.decay_rate = ms.Parameter(default_input = ms.Tensor(input_data=[[0.00]], dtype=ms.float32), requires_grad = False) # ICEWS18, 05, 0 requires_grad = False
        else:
            self.decay_rate = ms.Parameter(default_input = ms.Tensor(input_data=[[0.01]], dtype=ms.float32), requires_grad = True)
        if "ICEWS18" in self.dataset:
            self.trade_off = ms.Parameter(default_input = ms.Tensor(input_data=[[0.0]], dtype=ms.float32), requires_grad = False)
        else:
            #self.trade_off = torch.nn.Parameter(data = torch.cuda.FloatTensor(1,1), requires_grad = True)
            self.trade_off = ms.Parameter(default_input = ms.Tensor(dtype=ms.float32, shape=(1, 1), init=One()), requires_grad=True)
        # self.Transfer_SH = nn.Linear(self.numOfhidden, self.numOfhidden, bias=False)
        #
        # self.score_vector = torch.nn.Parameter(data=torch.cuda.FloatTensor(1, self.numOfhidden), requires_grad=True)
        # nn.init.xavier_uniform_(self.score_vector)
        #
        # self.auxiliary_matrix = nn.Linear(self.numOfhidden, self.numOfCommunity, bias=False)

        self.Transfer_SH = ms.nn.Dense(self.numOfhidden, self.numOfhidden, has_bias=False)
        
        self.score_vector = ms.Parameter(default_input=ms.Tensor(shape=(1, self.numOfhidden), dtype=ms.float32,
                                                                   init=XavierUniform()), requires_grad = True)
        #self.score_vector = initializer(XavierUniform(), self.score_vector.shape)

        self.auxiliary_matrix = ms.nn.Dense(self.numOfhidden, self.numOfCommunity, has_bias=False)

    # def forward(self, p_s, p_r, p_o, p_t, n_s, n_o, \
    #             s_h_r, s_h_e, s_h_t, \
    #             o_h_r, o_h_e, o_h_t, \
    #             p_s_d, p_o_d, p_t_m, \
    #             p_s_o_r \
    #             ):
    def construct(self, p_s, p_r, p_o, p_t, n_s, n_o, \
                s_h_r, s_h_e, s_h_t, \
                o_h_r, o_h_e, o_h_t, \
                p_s_d, p_o_d, p_t_m, \
                p_s_o_r \
                ):

        local_loss = self.get_local_loss(p_s, p_r, p_o, p_t, n_s, n_o, \
                                            s_h_r, s_h_e, s_h_t, \
                                            o_h_r, o_h_e, o_h_t, \
                                            )

        # s_h_e_flat = s_h_e.flatten(1)  # batch_size*(time_window*sample*sample)
        # o_h_e_flat = o_h_e.flatten(1)  # batch_size*(time_window*sample*sample)
        ms_flatten = ms.ops.Flatten()
        s_h_e_flat = ms_flatten(s_h_e) #batch_size*(time_window*sample*sample)
        o_h_e_flat = ms_flatten(o_h_e) #batch_size*(time_window*sample*sample)

        global_loss = self.get_global_loss(p_s, p_o, p_t, \
                                           n_s, n_o, \
                                           s_h_e_flat, o_h_e_flat, \
                                           p_s_d, p_o_d, p_t_m, \
                                           p_s_o_r)

        #co_loss = self.get_co_loss()

        batchLoss = local_loss + 0.01*global_loss# + co_loss

        return batchLoss

    def get_time_embedding_A(self, ind, t, dim):
        embedding_y1 = self.entity_embeddings_y1(ind)
        embedding_m1 = self.entity_embeddings_m1(ind)
        embedding_d1 = self.entity_embeddings_d1(ind)

        embedding_y2 = self.entity_embeddings_y2(ind)
        embedding_m2 = self.entity_embeddings_m2(ind)
        embedding_d2 = self.entity_embeddings_d2(ind)
        
        #embedding_period = (torch.cat([torch.sin(embedding_y1*(t//366 + 1)), torch.sin(embedding_m1*(t//30 + 1)), torch.sin(embedding_d1*(t%30 + 1))], -1))
        #embedding_nonper = (torch.cat([torch.tanh(embedding_y2*(t//366 + 1)), torch.tanh(embedding_m2*(t//30 + 1)), torch.tanh(embedding_d2*(t%30 + 1))], -1))

        # embedding_period = F.normalize(torch.cat([torch.sin(embedding_y1*(t//366 + 1)), torch.sin(embedding_m1*(t//30 + 1)), torch.sin(embedding_d1*(t%30 + 1))], -1), 2, -1)
        # embedding_nonper = F.normalize(torch.cat([torch.tanh(embedding_y2*(t//366 + 1)), torch.tanh(embedding_m2*(t//30 + 1)), torch.tanh(embedding_d2*(t%30 + 1))], -1), 2, -1)
        t_float32 = ms.ops.Cast()(t, ms.float32)
        embedding_period = ms.ops.L2Normalize(axis=-1)\
            (ms.ops.Concat(axis=-1)((ms.ops.sin(embedding_y1*(t_float32//366 + 1)),
                        ms.ops.sin(embedding_m1*(t_float32//30 + 1)),
                        ms.ops.sin(embedding_d1*(t_float32%30 + 1)))))
        embedding_nonper = ms.ops.L2Normalize(axis=-1)\
            (ms.ops.Concat(axis=-1)((ms.ops.tanh(embedding_y2*(t_float32//366 + 1)),
                        ms.ops.tanh(embedding_m2*(t_float32//30 + 1)),
                        ms.ops.tanh(embedding_d2*(t_float32%30 + 1)))))

        #embedding_period = F.normalize(torch.sin(embedding_y1*(t + 1)), 2, -1)
        #embedding_nonper = F.normalize(torch.tanh(embedding_y2*(t + 1)), 2, -1)
        embedding_static = self.entity_embeddings_v3(ind)
        #embedding = F.normalize(embedding_period + embedding_nonper + embedding_static, 2 ,dim)
        embedding = (embedding_period + embedding_nonper + embedding_static)
        #embedding = embedding_static
        #embedding = torch.cat([embedding_period, embedding_nonper, embedding_static], dim)

        return embedding

    def get_time_embedding_B(self, ind, t, dim):
        # embedding_y1 = self.entity_embeddings_y1(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        # embedding_m1 = self.entity_embeddings_m1(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        # embedding_d1 = self.entity_embeddings_d1(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        #
        # embedding_y2 = self.entity_embeddings_y2(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        # embedding_m2 = self.entity_embeddings_m2(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        # embedding_d2 = self.entity_embeddings_d2(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        embedding_y1 = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                           (ms.ops.ExpandDims()(self.entity_embeddings_y1(ind), 1), 1), 1)
        embedding_m1 = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                           (ms.ops.ExpandDims()(self.entity_embeddings_m1(ind), 1), 1), 1)
        embedding_d1 = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                           (ms.ops.ExpandDims()(self.entity_embeddings_d1(ind), 1), 1), 1)

        embedding_y2 = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                           (ms.ops.ExpandDims()(self.entity_embeddings_y2(ind), 1), 1), 1)
        embedding_m2 = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                           (ms.ops.ExpandDims()(self.entity_embeddings_m2(ind), 1), 1), 1)
        embedding_d2 = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                           (ms.ops.ExpandDims()(self.entity_embeddings_d2(ind), 1), 1), 1)
        
        #embedding_period = (torch.cat([torch.sin(embedding_y1*(t//366 + 1)), torch.sin(embedding_m1*(t//30 + 1)), torch.sin(embedding_d1*(t%30 + 1))], -1))
        #embedding_nonper = (torch.cat([torch.tanh(embedding_y2*(t//366 + 1)), torch.tanh(embedding_m2*(t//30 + 1)), torch.tanh(embedding_d2*(t%30 + 1))], -1))
        # embedding_period = F.normalize(torch.cat(
        #     [torch.sin(embedding_y1 * (t // 366 + 1)), torch.sin(embedding_m1 * (t // 30 + 1)),
        #      torch.sin(embedding_d1 * (t % 30 + 1))], -1), 2, -1)
        # embedding_nonper = F.normalize(torch.cat(
        #     [torch.tanh(embedding_y2 * (t // 366 + 1)), torch.tanh(embedding_m2 * (t // 30 + 1)),
        #      torch.tanh(embedding_d2 * (t % 30 + 1))], -1), 2, -1)

        embedding_period = ms.ops.L2Normalize(axis=-1)(ms.ops.Concat(axis=-1)
                                                       ((ms.ops.sin(embedding_y1*(t//366 + 1)),
                                                         ms.ops.sin(embedding_m1*(t//30 + 1)),
                                                         ms.ops.sin(embedding_d1*(t%30 + 1)))))
        embedding_nonper = ms.ops.L2Normalize(axis=-1)(ms.ops.Concat(axis=-1)
                                                       ((ms.ops.tanh(embedding_y2*(t//366 + 1)),
                                                         ms.ops.tanh(embedding_m2*(t//30 + 1)),
                                                         ms.ops.tanh(embedding_d2*(t%30 + 1)))))

        #embedding_period = F.normalize(torch.sin(embedding_y1*(t + 1)), 2, -1)
        #embedding_nonper = F.normalize(torch.tanh(embedding_y2*(t + 1)), 2, -1)
        # embedding_static = self.entity_embeddings_v3(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        # embedding_static = embedding_static.repeat(1, embedding_period.size()[1], embedding_period.size()[2], embedding_period.size()[3], 1)

        embedding_static = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                               (ms.ops.ExpandDims()(self.entity_embeddings_v3(ind), 1), 1), 1)
        embedding_static = embedding_static.repeat(embedding_period.shape[1], axis=1)
        embedding_static = embedding_static.repeat(embedding_period.shape[2], axis=2)
        embedding_static = embedding_static.repeat(embedding_period.shape[3], axis=3)
        #embedding = F.normalize(embedding_period + embedding_nonper + embedding_static, 2 ,dim)
        embedding = (embedding_period + embedding_nonper + embedding_static)
        #embedding = embedding_static
        #embedding = torch.cat([embedding_period, embedding_nonper, embedding_static], dim)

        return embedding

    def get_time_embedding_B_lowdim(self, ind, t, dim):
        # embedding_y1 = self.entity_embeddings_y1(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        # embedding_m1 = self.entity_embeddings_m1(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        # embedding_d1 = self.entity_embeddings_d1(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        #
        # embedding_y2 = self.entity_embeddings_y2(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        # embedding_m2 = self.entity_embeddings_m2(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        # embedding_d2 = self.entity_embeddings_d2(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        embedding_y1 = self.entity_embeddings_y1(ind)
        embedding_m1 = self.entity_embeddings_m1(ind)
        embedding_d1 = self.entity_embeddings_d1(ind)

        embedding_y2 = self.entity_embeddings_y2(ind)
        embedding_m2 = self.entity_embeddings_m2(ind)
        embedding_d2 = self.entity_embeddings_d2(ind)

        # embedding_period = (torch.cat([torch.sin(embedding_y1*(t//366 + 1)), torch.sin(embedding_m1*(t//30 + 1)), torch.sin(embedding_d1*(t%30 + 1))], -1))
        # embedding_nonper = (torch.cat([torch.tanh(embedding_y2*(t//366 + 1)), torch.tanh(embedding_m2*(t//30 + 1)), torch.tanh(embedding_d2*(t%30 + 1))], -1))
        # embedding_period = F.normalize(torch.cat(
        #     [torch.sin(embedding_y1 * (t // 366 + 1)), torch.sin(embedding_m1 * (t // 30 + 1)),
        #      torch.sin(embedding_d1 * (t % 30 + 1))], -1), 2, -1)
        # embedding_nonper = F.normalize(torch.cat(
        #     [torch.tanh(embedding_y2 * (t // 366 + 1)), torch.tanh(embedding_m2 * (t // 30 + 1)),
        #      torch.tanh(embedding_d2 * (t % 30 + 1))], -1), 2, -1)

        embedding_period = ms.ops.L2Normalize(axis=-1)(ms.ops.Concat(axis=-1)
                                                       ((ms.ops.sin(embedding_y1 * (t // 366 + 1)),
                                                         ms.ops.sin(embedding_m1 * (t // 30 + 1)),
                                                         ms.ops.sin(embedding_d1 * (t % 30 + 1)))))
        embedding_nonper = ms.ops.L2Normalize(axis=-1)(ms.ops.Concat(axis=-1)
                                                       ((ms.ops.tanh(embedding_y2 * (t // 366 + 1)),
                                                         ms.ops.tanh(embedding_m2 * (t // 30 + 1)),
                                                         ms.ops.tanh(embedding_d2 * (t % 30 + 1)))))

        # embedding_period = F.normalize(torch.sin(embedding_y1*(t + 1)), 2, -1)
        # embedding_nonper = F.normalize(torch.tanh(embedding_y2*(t + 1)), 2, -1)
        # embedding_static = self.entity_embeddings_v3(ind).unsqueeze(1).unsqueeze(1).unsqueeze(1)
        # embedding_static = embedding_static.repeat(1, embedding_period.size()[1], embedding_period.size()[2], embedding_period.size()[3], 1)

        embedding_static = self.entity_embeddings_v3(ind)
        # embedding_static = embedding_static.repeat(embedding_period.shape[1], axis=1)
        # embedding_static = embedding_static.repeat(embedding_period.shape[2], axis=2)
        #embedding_static = embedding_static.repeat(embedding_period.shape[3], axis=3)
        # embedding = F.normalize(embedding_period + embedding_nonper + embedding_static, 2 ,dim)
        embedding = (embedding_period + embedding_nonper + embedding_static)
        # embedding = embedding_static
        # embedding = torch.cat([embedding_period, embedding_nonper, embedding_static], dim)
        #embedding = ms.ops.expand_dims(embedding.reshape([-1, embedding.shape[2], embedding.shape[3]]), 1)
        return embedding

    def get_time_embedding_C(self, ind, t, dim):

        # embedding_y1 = self.entity_embeddings_y1(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        # embedding_m1 = self.entity_embeddings_m1(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        # embedding_d1 = self.entity_embeddings_d1(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        #
        # embedding_y2 = self.entity_embeddings_y2(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        # embedding_m2 = self.entity_embeddings_m2(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        # embedding_d2 = self.entity_embeddings_d2(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        embedding_y1 = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                           (ms.ops.ExpandDims()
                                            (self.entity_embeddings_y1(ind), 2), 2), 2)
        embedding_m1 = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                           (ms.ops.ExpandDims()
                                            (self.entity_embeddings_m1(ind), 2), 2), 2)
        embedding_d1 = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                           (ms.ops.ExpandDims()
                                            (self.entity_embeddings_d1(ind), 2), 2), 2)

        embedding_y2 = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                           (ms.ops.ExpandDims()
                                            (self.entity_embeddings_y2(ind), 2), 2), 2)
        embedding_m2 = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                           (ms.ops.ExpandDims()
                                            (self.entity_embeddings_m2(ind), 2), 2), 2)
        embedding_d2 = ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                           (ms.ops.ExpandDims()
                                            (self.entity_embeddings_d2(ind), 2), 2), 2)
        
        #embedding_period = (torch.cat([torch.sin(embedding_y1*(t//366 + 1)), torch.sin(embedding_m1*(t//30 + 1)), torch.sin(embedding_d1*(t%30 + 1))], -1))
        #embedding_nonper = (torch.cat([torch.tanh(embedding_y2*(t//366 + 1)), torch.tanh(embedding_m2*(t//30 + 1)), torch.tanh(embedding_d2*(t%30 + 1))], -1))

        # embedding_period = F.normalize(torch.cat([torch.sin(embedding_y1*(t//366 + 1)), torch.sin(embedding_m1*(t//30 + 1)), torch.sin(embedding_d1*(t%30 + 1))], -1), 2, -1)
        # embedding_nonper = F.normalize(torch.cat([torch.tanh(embedding_y2*(t//366 + 1)), torch.tanh(embedding_m2*(t//30 + 1)), torch.tanh(embedding_d2*(t%30 + 1))], -1), 2, -1)
        # #embedding_period = F.normalize(torch.sin(embedding_y1*(t + 1)), 2, -1)
        # #embedding_nonper = F.normalize(torch.tanh(embedding_y2*(t + 1)), 2, -1)
        # embedding_static = self.entity_embeddings_v3(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        # embedding_static = embedding_static.repeat(1, 1, embedding_period.size()[2], embedding_period.size()[3], embedding_period.size()[4], 1)


        embedding_period = ms.ops.L2Normalize(axis=-1)(ms.ops.Concat(axis=-1)((ms.ops.sin(embedding_y1*(t//366 + 1)),
                                                                               ms.ops.sin(embedding_m1*(t//30 + 1)),
                                                                               ms.ops.sin(embedding_d1*(t%30 + 1)))))
        embedding_nonper = ms.ops.L2Normalize(axis=-1)(ms.ops.Concat(axis=-1)((ms.ops.tanh(embedding_y2*(t//366 + 1)),
                                                                               ms.ops.tanh(embedding_m2*(t//30 + 1)),
                                                                               ms.ops.tanh(embedding_d2*(t%30 + 1)))))
        #embedding_period = F.normalize(torch.sin(embedding_y1*(t + 1)), 2, -1)
        #embedding_nonper = F.normalize(torch.tanh(embedding_y2*(t + 1)), 2, -1)
        embedding_static = ms.ops.ExpandDims()(ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                                                   (self.entity_embeddings_v3(ind), 2), 2), 2)
        embedding_static = embedding_static.repeat(embedding_period.shape[2], axis=2)
        embedding_static = embedding_static.repeat(embedding_period.shape[3], axis=3)
        embedding_static = embedding_static.repeat(embedding_period.shape[4], axis=4)

        #embedding = F.normalize(embedding_period + embedding_nonper + embedding_static, 2 ,dim)
        embedding = (embedding_period + embedding_nonper + embedding_static)
        #embedding = embedding_static
        #embedding = torch.cat([embedding_period, embedding_nonper, embedding_static], dim)

        return embedding

    def get_time_embedding_C_lowdim(self, ind, t, dim):

        # embedding_y1 = self.entity_embeddings_y1(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        # embedding_m1 = self.entity_embeddings_m1(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        # embedding_d1 = self.entity_embeddings_d1(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        #
        # embedding_y2 = self.entity_embeddings_y2(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        # embedding_m2 = self.entity_embeddings_m2(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        # embedding_d2 = self.entity_embeddings_d2(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        embedding_y1 = self.entity_embeddings_y1(ind)
        embedding_m1 = self.entity_embeddings_m1(ind)
        embedding_d1 = self.entity_embeddings_d1(ind)

        embedding_y2 = self.entity_embeddings_y2(ind)
        embedding_m2 = self.entity_embeddings_m2(ind)
        embedding_d2 = self.entity_embeddings_d2(ind)

        # embedding_period = (torch.cat([torch.sin(embedding_y1*(t//366 + 1)), torch.sin(embedding_m1*(t//30 + 1)), torch.sin(embedding_d1*(t%30 + 1))], -1))
        # embedding_nonper = (torch.cat([torch.tanh(embedding_y2*(t//366 + 1)), torch.tanh(embedding_m2*(t//30 + 1)), torch.tanh(embedding_d2*(t%30 + 1))], -1))

        # embedding_period = F.normalize(torch.cat([torch.sin(embedding_y1*(t//366 + 1)), torch.sin(embedding_m1*(t//30 + 1)), torch.sin(embedding_d1*(t%30 + 1))], -1), 2, -1)
        # embedding_nonper = F.normalize(torch.cat([torch.tanh(embedding_y2*(t//366 + 1)), torch.tanh(embedding_m2*(t//30 + 1)), torch.tanh(embedding_d2*(t%30 + 1))], -1), 2, -1)
        # #embedding_period = F.normalize(torch.sin(embedding_y1*(t + 1)), 2, -1)
        # #embedding_nonper = F.normalize(torch.tanh(embedding_y2*(t + 1)), 2, -1)
        # embedding_static = self.entity_embeddings_v3(ind).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        # embedding_static = embedding_static.repeat(1, 1, embedding_period.size()[2], embedding_period.size()[3], embedding_period.size()[4], 1)

        embedding_period = ms.ops.L2Normalize(axis=-1)(
            ms.ops.Concat(axis=-1)((ms.ops.sin(embedding_y1 * (t // 366 + 1)),
                                    ms.ops.sin(embedding_m1 * (t // 30 + 1)),
                                    ms.ops.sin(embedding_d1 * (t % 30 + 1)))))
        embedding_nonper = ms.ops.L2Normalize(axis=-1)(
            ms.ops.Concat(axis=-1)((ms.ops.tanh(embedding_y2 * (t // 366 + 1)),
                                    ms.ops.tanh(embedding_m2 * (t // 30 + 1)),
                                    ms.ops.tanh(embedding_d2 * (t % 30 + 1)))))
        # embedding_period = F.normalize(torch.sin(embedding_y1*(t + 1)), 2, -1)
        # embedding_nonper = F.normalize(torch.tanh(embedding_y2*(t + 1)), 2, -1)
        embedding_static = self.entity_embeddings_v3(ind)
        # embedding_static = embedding_static.repeat(embedding_period.shape[2], axis=2)
        # embedding_static = embedding_static.repeat(embedding_period.shape[3], axis=3)
        # embedding_static = embedding_static.repeat(embedding_period.shape[4], axis=4)

        # embedding = F.normalize(embedding_period + embedding_nonper + embedding_static, 2 ,dim)
        embedding = (embedding_period + embedding_nonper + embedding_static)
        # embedding = embedding_static
        # embedding = torch.cat([embedding_period, embedding_nonper, embedding_static], dim)

        return embedding

    def get_time_embedding_D(self, t, dim):

        # embedding_y1 = self.entity_embeddings_y1.weight.data[0:self.numOfEntity].unsqueeze(0)
        # embedding_m1 = self.entity_embeddings_m1.weight.data[0:self.numOfEntity].unsqueeze(0)
        # embedding_d1 = self.entity_embeddings_d1.weight.data[0:self.numOfEntity].unsqueeze(0)
        #
        # embedding_y2 = self.entity_embeddings_y2.weight.data[0:self.numOfEntity].unsqueeze(0)
        # embedding_m2 = self.entity_embeddings_m2.weight.data[0:self.numOfEntity].unsqueeze(0)
        # embedding_d2 = self.entity_embeddings_d2.weight.data[0:self.numOfEntity].unsqueeze(0)

        embedding_y1 = ms.ops.expand_dims(self.entity_embeddings_y1.embedding_table.data[0:self.numOfEntity], 0)
        embedding_m1 = ms.ops.expand_dims(self.entity_embeddings_m1.embedding_table.data[0:self.numOfEntity], 0)
        embedding_d1 = ms.ops.expand_dims(self.entity_embeddings_d1.embedding_table.data[0:self.numOfEntity], 0)

        embedding_y2 = ms.ops.expand_dims(self.entity_embeddings_y2.embedding_table.data[0:self.numOfEntity], 0)
        embedding_m2 = ms.ops.expand_dims(self.entity_embeddings_m2.embedding_table.data[0:self.numOfEntity], 0)
        embedding_d2 = ms.ops.expand_dims(self.entity_embeddings_d2.embedding_table.data[0:self.numOfEntity], 0)
        
        #embedding_period = (torch.cat([torch.sin(embedding_y1*(t//366 + 1)), torch.sin(embedding_m1*(t//30 + 1)), torch.sin(embedding_d1*(t%30 + 1))], -1))
        #embedding_nonper = (torch.cat([torch.tanh(embedding_y2*(t//366 + 1)), torch.tanh(embedding_m2*(t//30 + 1)), torch.tanh(embedding_d2*(t%30 + 1))], -1))

        # embedding_period = F.normalize(torch.cat(
        #     [torch.sin(embedding_y1 * (t // 366 + 1)), torch.sin(embedding_m1 * (t // 30 + 1)),
        #      torch.sin(embedding_d1 * (t % 30 + 1))], -1), 2, -1)
        # embedding_nonper = F.normalize(torch.cat(
        #     [torch.tanh(embedding_y2 * (t // 366 + 1)), torch.tanh(embedding_m2 * (t // 30 + 1)),
        #      torch.tanh(embedding_d2 * (t % 30 + 1))], -1), 2, -1)
        embedding_period = ms.ops.L2Normalize(axis=-1)(
            ms.ops.Concat(axis=-1)((ms.ops.sin(embedding_y1*(t//366 + 1)),
                                    ms.ops.sin(embedding_m1*(t//30 + 1)),
                                    ms.ops.sin(embedding_d1*(t%30 + 1)))))
        embedding_nonper = ms.ops.L2Normalize(axis=-1)(
            ms.ops.Concat(axis=-1)((ms.ops.tanh(embedding_y2*(t//366 + 1)),
                                    ms.ops.tanh(embedding_m2*(t//30 + 1)),
                                    ms.ops.tanh(embedding_d2*(t%30 + 1)))))
        #embedding_period = F.normalize(torch.sin(embedding_y1*(t + 1)), 2, -1)
        #embedding_nonper = F.normalize(torch.tanh(embedding_y2*(t + 1)), 2, -1)
        embedding_static = ms.ops.expand_dims(self.entity_embeddings_v3.embedding_table.data[0:self.numOfEntity], 0)
        #embedding_static = embedding_static.repeat(embedding_period.size()[0], 1, 1)
        embedding_static = embedding_static.repeat(embedding_period.shape[0], axis=0)
        #embedding = F.normalize(embedding_period + embedding_nonper + embedding_static, 2 ,dim)
        embedding = (embedding_period + embedding_nonper + embedding_static)
        #embedding = embedding_static
        #embedding = torch.cat([embedding_period, embedding_nonper, embedding_static], dim)

        return embedding

    def get_time_embedding_E(self, t, dim):
        embedding_y1 = self.entity_embeddings_y1.weight.data[0:self.numOfEntity].unsqueeze(0).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        embedding_m1 = self.entity_embeddings_m1.weight.data[0:self.numOfEntity].unsqueeze(0).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        embedding_d1 = self.entity_embeddings_d1.weight.data[0:self.numOfEntity].unsqueeze(0).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        
        embedding_y2 = self.entity_embeddings_y2.weight.data[0:self.numOfEntity].unsqueeze(0).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        embedding_m2 = self.entity_embeddings_m2.weight.data[0:self.numOfEntity].unsqueeze(0).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        embedding_d2 = self.entity_embeddings_d2.weight.data[0:self.numOfEntity].unsqueeze(0).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        
        
        #embedding_period = (torch.cat([torch.sin(embedding_y1*(t//366 + 1)), torch.sin(embedding_m1*(t//30 + 1)), torch.sin(embedding_d1*(t%30 + 1))], -1))
        #embedding_nonper = (torch.cat([torch.tanh(embedding_y2*(t//366 + 1)), torch.tanh(embedding_m2*(t//30 + 1)), torch.tanh(embedding_d2*(t%30 + 1))], -1))
        embedding_period = F.normalize(torch.cat([torch.sin(embedding_y1*(t//366 + 1)), torch.sin(embedding_m1*(t//30 + 1)), torch.sin(embedding_d1*(t%30 + 1))], -1), 2, -1)
        embedding_nonper = F.normalize(torch.cat([torch.tanh(embedding_y2*(t//366 + 1)), torch.tanh(embedding_m2*(t//30 + 1)), torch.tanh(embedding_d2*(t%30 + 1))], -1), 2, -1)
        #embedding_period = F.normalize(torch.sin(embedding_y1*(t + 1)), 2, -1)
        #embedding_nonper = F.normalize(torch.tanh(embedding_y2*(t + 1)), 2, -1)
        embedding_static = self.entity_embeddings_v3.weight.data[0:self.numOfEntity].unsqueeze(0).unsqueeze(2).unsqueeze(2).unsqueeze(2)
        embedding_static = embedding_static.repeat(embedding_period.size()[0], 1, embedding_period.size()[2], embedding_period.size()[3], embedding_period.size()[4], 1)
        #embedding = F.normalize(embedding_period + embedding_nonper + embedding_static, 2 ,dim)
        embedding = (embedding_period + embedding_nonper + embedding_static)
        #embedding = embedding_static
        #embedding = torch.cat([embedding_period, embedding_nonper, embedding_static], dim)
        
        return embedding

    def get_time_embedding_E_lowdim(self, t, dim):
        embedding_y1 = ms.ops.expand_dims(self.entity_embeddings_y1.embedding_table.data[0:self.numOfEntity], 0)
        embedding_m1 = ms.ops.expand_dims(self.entity_embeddings_m1.embedding_table.data[0:self.numOfEntity], 0)
        embedding_d1 = ms.ops.expand_dims(self.entity_embeddings_d1.embedding_table.data[0:self.numOfEntity], 0)

        embedding_y2 = ms.ops.expand_dims(self.entity_embeddings_y2.embedding_table.data[0:self.numOfEntity], 0)
        embedding_m2 = ms.ops.expand_dims(self.entity_embeddings_m2.embedding_table.data[0:self.numOfEntity], 0)
        embedding_d2 = ms.ops.expand_dims(self.entity_embeddings_d2.embedding_table.data[0:self.numOfEntity], 0)

        # embedding_period = (torch.cat([torch.sin(embedding_y1*(t//366 + 1)), torch.sin(embedding_m1*(t//30 + 1)), torch.sin(embedding_d1*(t%30 + 1))], -1))
        # embedding_nonper = (torch.cat([torch.tanh(embedding_y2*(t//366 + 1)), torch.tanh(embedding_m2*(t//30 + 1)), torch.tanh(embedding_d2*(t%30 + 1))], -1))
        embedding_period = ms.ops.L2Normalize(axis=-1)(
            ms.ops.Concat(axis=-1)(
            (ms.ops.sin(embedding_y1 * (t // 366 + 1)),
             ms.ops.sin(embedding_m1 * (t // 30 + 1)),
             ms.ops.sin(embedding_d1 * (t % 30 + 1)))))
        embedding_nonper = ms.ops.L2Normalize(axis=-1)(
            ms.ops.Concat(axis=-1)(
                (ms.ops.tanh(embedding_y2 * (t // 366 + 1)),
                 ms.ops.tanh(embedding_m2 * (t // 30 + 1)),
                 ms.ops.tanh(embedding_d2 * (t % 30 + 1)))))
        # embedding_period = F.normalize(torch.sin(embedding_y1*(t + 1)), 2, -1)
        # embedding_nonper = F.normalize(torch.tanh(embedding_y2*(t + 1)), 2, -1)
        embedding_static = ms.ops.expand_dims(self.entity_embeddings_v3.embedding_table.data[0:self.numOfEntity], 0)
        embedding_static = embedding_static.repeat(embedding_period.shape[0], axis=0)
        # embedding_static = embedding_static.repeat(embedding_period.size()[0], 1, embedding_period.size()[2],
        #                                            embedding_period.size()[3], embedding_period.size()[4], 1)
        # embedding = F.normalize(embedding_period + embedding_nonper + embedding_static, 2 ,dim)
        embedding = (embedding_period + embedding_nonper + embedding_static)
        # embedding = embedding_static
        # embedding = torch.cat([embedding_period, embedding_nonper, embedding_static], dim)

        return embedding


    def masked_softmax(self, A, B, k, dim):

        # A = A.float()
        # A_max = torch.max(A, dim=dim, keepdim=True)[0]
        # A_exp = torch.exp(A - A_max)
        # A_exp = A_exp * (B != k).float()
        # Sum = torch.sum(A_exp, dim=dim, keepdim=True)
        A = ms.ops.Cast()(A, ms.float32)
        _, A_max = ms.ops.ArgMaxWithValue(axis=dim, keep_dims=True)(A)
        A_max = A_max[0]
        A_exp = ms.ops.exp(A-A_max)
        A_exp = A_exp * ms.ops.Cast()(B != k, ms.float32)
        Sum = ms.ops.ReduceSum(keep_dims=True)(A_exp, dim)
        if "forecast" in self.dataset:
            if "ICEWS18" in self.dataset:
                #Sum = Sum+(Sum == 0.0).float()
                Sum = Sum+ms.ops.Cast()(Sum == 0.0, ms.float32)
            else:
                Sum = Sum+0.01
        else:
            if self.dataset == "ICEWS14":
                Sum = Sum+0.1
            if self.dataset == "ICEWS05":
                Sum = Sum+0.01
            else:
                #Sum = Sum+(Sum == 0.0).float()
                Sum = Sum+ms.ops.Cast()(Sum == 0.0, ms.float32)
        score = A_exp / Sum
        
        '''
        A = A.float()
        A_max = torch.max(A,dim=dim,keepdim=True)[0]
        A_exp = torch.exp(A-A_max)
        A_exp = A_exp * (A != 0).float()
        Sum = torch.sum(A_exp,dim=dim,keepdim=True)
        Sum = Sum + (Sum == 0.0).float()
        score = A_exp / Sum
        '''
        #score = nn.Softmax(dim)(A)
        #score = nn.Softmax(dim)(A)
        
        return score

    def get_local_loss(self, p_s, p_r, p_o, p_t, n_s, n_o, s_h_r, s_h_e, s_h_t, o_h_r, o_h_e, o_h_t):

        batch_size = o_h_e.shape[0]
        time_window_size = o_h_e.shape[1]

        ent_norm = 0
        # get base intensity of pos and neg facts
        # p_s_embedding = self.get_time_embedding_A(p_s, p_t.unsqueeze(1), 1)  # , 2, 1)
        #
        # p_o_embedding = self.get_time_embedding_A(p_o, p_t.unsqueeze(1), 1)  # , 2, 1)
        #
        # n_s_embedding = self.get_time_embedding_A(n_s, p_t.unsqueeze(1).unsqueeze(1), 2)  # , 2, 2)
        #
        # n_o_embedding = self.get_time_embedding_A(n_o, p_t.unsqueeze(1).unsqueeze(1), 2)  # , 2, 2)

        p_s_embedding = self.get_time_embedding_A(p_s, ms.ops.ExpandDims()(p_t, 1), 1)#, 2, 1)

        p_o_embedding = self.get_time_embedding_A(p_o, ms.ops.ExpandDims()(p_t, 1), 1)#, 2, 1)

        n_s_embedding = self.get_time_embedding_A(n_s, ms.ops.ExpandDims()(ms.ops.ExpandDims()(p_t, 1), 1), 2)#, 2, 2)

        n_o_embedding = self.get_time_embedding_A(n_o, ms.ops.ExpandDims()(ms.ops.ExpandDims()(p_t, 1), 1), 2)#, 2, 2)

        p_r_embedding = self.relation_embeddings(p_r) # batch_size*hidden

        '''
        p_base_score = F.dropout(p_s_embedding + p_r_embedding - p_o_embedding, p=self.prob)#batch_size
        p_base_score = torch.sum(p_base_score**2, 1).neg()
        ns_base_score = F.dropout(n_s_embedding + p_r_embedding.unsqueeze(1) - p_o_embedding.unsqueeze(1), p=self.prob)#batch_size*ns
        ns_base_score = torch.sum(ns_base_score**2, 2).neg()
        no_base_score = F.dropout(p_s_embedding.unsqueeze(1) + p_r_embedding.unsqueeze(1) - n_o_embedding, p=self.prob)
        no_base_score = torch.sum(no_base_score**2, 2).neg()
        '''
        '''
        p_base_emb = F.dropout(p_s_embedding * p_r_embedding * p_o_embedding, p=self.prob)#batch_size
        p_base_score = torch.sum(p_base_emb, 1)#/torch.norm(p_base_emb, 2, 1)
        ns_base_emb = F.dropout(n_s_embedding * p_r_embedding.unsqueeze(1) * p_o_embedding.unsqueeze(1), p=self.prob)#batch_size*ns
        ns_base_score = torch.sum(ns_base_emb, 2)#/torch.norm(ns_base_emb, 2, 2)
        no_base_emb = F.dropout(p_s_embedding.unsqueeze(1) * p_r_embedding.unsqueeze(1) * n_o_embedding, p=self.prob)
        no_base_score = torch.sum(no_base_emb, 2)#/torch.norm(no_base_emb, 2, 2)
        '''

        # p_base_score = (self.Transfer_SH(p_s_embedding + p_r_embedding))  # batch_size
        # p_base_score = torch.sum(p_o_embedding * p_base_score, 1)  # .neg()
        # ns_base_score = (self.Transfer_SH(n_s_embedding + p_r_embedding.unsqueeze(1)))  # batch_size*ns
        # ns_base_score = torch.sum(p_o_embedding.unsqueeze(1) * ns_base_score, 2)  # .neg()
        # no_base_score = (self.Transfer_SH(p_s_embedding + p_r_embedding))
        # no_base_score = torch.sum(n_o_embedding * no_base_score.unsqueeze(1), 2)  # .neg()
        p_base_score = (self.Transfer_SH(p_s_embedding + p_r_embedding)) #batch_size
        p_base_score = ms.ops.ReduceSum()(p_o_embedding*p_base_score, 1)#.neg()
        ns_base_score = (self.Transfer_SH(n_s_embedding + ms.ops.ExpandDims()(p_r_embedding, 1))) #batch_size*ns
        ns_base_score = ms.ops.ReduceSum()(ms.ops.ExpandDims()(p_o_embedding, 1)*ns_base_score, 2)#.neg()
        no_base_score = (self.Transfer_SH(p_s_embedding + p_r_embedding))
        no_base_score = ms.ops.ReduceSum()(n_o_embedding*ms.ops.ExpandDims()(no_base_score, 1), 2)#.neg()

        o_h_e = o_h_e.reshape([-1, o_h_e.shape[2], o_h_e.shape[3]])
        o_h_r = o_h_r.reshape([-1, o_h_r.shape[2]])
        o_h_t = o_h_t.reshape([-1])

        s_h_e = s_h_e.reshape([-1, s_h_e.shape[2], s_h_e.shape[3]])
        s_h_r = s_h_r.reshape([-1, s_h_r.shape[2]])
        s_h_t = s_h_t.reshape([-1])

        p_s = p_s.repeat(time_window_size, axis=0)
        p_r = p_r.repeat(time_window_size, axis=0)
        p_o = p_o.repeat(time_window_size, axis=0)
        p_t = p_t.repeat(time_window_size, axis=0)

        n_s = n_s.repeat(time_window_size, axis=0)
        n_o = n_o.repeat(time_window_size, axis=0)

        p_r_embedding = p_r_embedding.repeat(time_window_size, axis=0)

        # p_s_embedding = self.get_time_embedding_A(p_s, ms.ops.ExpandDims()(p_t, 1), 1)  # , 2, 1)
        #
        # p_o_embedding = self.get_time_embedding_A(p_o, ms.ops.ExpandDims()(p_t, 1), 1)  # , 2, 1)
        #
        # n_s_embedding = self.get_time_embedding_A(n_s, ms.ops.ExpandDims()(ms.ops.ExpandDims()(p_t, 1), 1),
        #                                           2)  # , 2, 2)
        #
        # n_o_embedding = self.get_time_embedding_A(n_o, ms.ops.ExpandDims()(ms.ops.ExpandDims()(p_t, 1), 1),
        #                                           2)  # , 2, 2)

        # get history of head entity
        # s_h_r_embedding = self.relation_embeddings(s_h_r) #batch_size*time_window*relation_num(sample)*hidden
        # s_h_e_embedding = self.get_time_embedding_A(s_h_e, s_h_t.unsqueeze(2).unsqueeze(2).unsqueeze(2), 4) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        # ent_norm += Loss.normLoss(s_h_e_embedding, 4)
        # o_his_embedding = self.get_time_embedding_B(p_o, s_h_t.unsqueeze(2).unsqueeze(2).unsqueeze(2), 4) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        # ent_norm += Loss.normLoss(o_his_embedding, 4)
        # time_decay = torch.exp(-torch.abs(self.decay_rate)*torch.abs(p_t.unsqueeze(1) - s_h_t)) #batch_size*time_window

        s_h_r_embedding = self.relation_embeddings(s_h_r) #batch_size*time_window*relation_num(sample)*hidden
        s_h_e_embedding = self.get_time_embedding_A(s_h_e, ms.ops.expand_dims(ms.ops.expand_dims
                                                                              (ms.ops.expand_dims(s_h_t, 1), 1), 1), 4) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        ent_norm += Loss.normLoss(s_h_e_embedding, 3)
        o_his_embedding = self.get_time_embedding_B_lowdim(p_o, ms.ops.expand_dims(s_h_t, 1), 1) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        ent_norm += Loss.normLoss(o_his_embedding, 1)
        time_decay = ms.ops.exp(-ms.ops.abs(self.decay_rate)*ms.ops.abs(p_t - s_h_t)) #batch_size*time_window

        # #s_score = torch.sum((s_h_e_embedding - o_his_embedding)**2, 4).neg() + torch.sum(o_his_embedding**2, 4) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        # s_score = torch.sum(self.Transfer_E(s_h_e_embedding)*o_his_embedding, 4)
        # s_att = self.masked_softmax(s_score, s_h_e, self.numOfEntity, 3) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        # #print(s_att[0][0][0])
        # s_his_score = torch.sum(s_score*s_att, 3) # + torch.mean(torch.norm(o_his_embedding, self.norm, 4), 3) # + (s_h_r == self.numOfRelation).float() #batch_size*time_window*relation_sum(sample)


        #s_score = torch.sum((s_h_e_embedding - o_his_embedding)**2, 4).neg() + torch.sum(o_his_embedding**2, 4) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        o_his_embedding = ms.ops.expand_dims(ms.ops.expand_dims(o_his_embedding, 1), 1)
        s_score = ms.ops.ReduceSum()(self.Transfer_E(s_h_e_embedding)*o_his_embedding, 3)
        s_att = self.masked_softmax(s_score, s_h_e, self.numOfEntity, 2) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        #print(s_att[0][0][0])
        s_his_score = ms.ops.ReduceSum()(s_score*s_att, 2) # + torch.mean(torch.norm(o_his_embedding, self.norm, 4), 3) # + (s_h_r == self.numOfRelation).float() #batch_size*time_window*relation_sum(sample)

        # r_score_s = torch.sum(self.Transfer_R(p_r_embedding).unsqueeze(1).unsqueeze(1) * s_h_r_embedding,
        #                       3)  # batch_size*time_window*relation_sum(sample)
        # r_att_s = self.masked_softmax(r_score_s, s_h_r, self.numOfRelation,
        #                               2)  # batch_size*time_window*relation_sum(sample)
        # s_his_score = torch.sum(s_his_score * r_att_s, 2)  # + 1#*(time_decay == 1).float() #batch_size*time_window
        #
        # s_his_score = torch.sum(s_his_score * time_decay, 1)  # batch_size
        r_score_s = ms.ops.ReduceSum()(ms.ops.expand_dims(self.Transfer_R(p_r_embedding), 1)
                                       *s_h_r_embedding, 2) #batch_size*time_window*relation_sum(sample)
        r_att_s = self.masked_softmax(r_score_s, s_h_r, self.numOfRelation, 1) #batch_size*time_window*relation_sum(sample)
        s_his_score = ms.ops.ReduceSum()(s_his_score*r_att_s, 1) # + 1#*(time_decay == 1).float() #batch_size*time_window

        # s_his_score = ms.ops.ReduceSum()(s_his_score*time_decay.reshape([-1]), 1) #batch_size
        s_his_score = ms.ops.ReduceSum()(s_his_score.reshape([batch_size, -1]) * time_decay.reshape([batch_size, -1]), 1)  # batch_size
        #s_his_score = s_his_score + 0.5*(s_his_score == 0.0).float()


        # get history of tail entity
        # o_h_r_embedding = self.relation_embeddings(o_h_r)  # batch_size*time_window*relation_num(sample)*hidden
        # o_h_e_embedding = self.get_time_embedding_A(o_h_e, o_h_t.unsqueeze(2).unsqueeze(2).unsqueeze(2),
        #                                             4)  # batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        # ent_norm += Loss.normLoss(o_h_e_embedding, 4)
        # s_his_embedding = self.get_time_embedding_B(p_s, o_h_t.unsqueeze(2).unsqueeze(2).unsqueeze(2),
        #                                             4)  # batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        # ent_norm += Loss.normLoss(s_his_embedding, 4)
        # time_decay = torch.exp(
        #     -torch.abs(self.decay_rate) * torch.abs(p_t.unsqueeze(1) - o_h_t))  # batch_size*time_window
        o_h_r_embedding = self.relation_embeddings(o_h_r) #batch_size*time_window*relation_num(sample)*hidden
        o_h_e_embedding = self.get_time_embedding_A(o_h_e, ms.ops.ExpandDims()(ms.ops.ExpandDims()
                                                                               (ms.ops.ExpandDims()
                                                                                (o_h_t, 1), 1), 1), 4) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        ent_norm += Loss.normLoss(o_h_e_embedding, 3)
        s_his_embedding = self.get_time_embedding_B_lowdim(p_s, ms.ops.expand_dims(o_h_t, 1), 1) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        ent_norm += Loss.normLoss(s_his_embedding, 1)
        time_decay = ms.ops.exp(-ms.ops.abs(self.decay_rate)*ms.ops.abs(p_t - o_h_t)) #batch_size*time_window

        # #o_score = torch.sum((o_h_e_embedding - s_his_embedding)**2, 4).neg() + torch.sum(s_his_embedding**2, 4) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        # o_score = torch.sum(self.Transfer_E(o_h_e_embedding)*s_his_embedding, 4)
        # o_att = self.masked_softmax(o_score, o_h_e, self.numOfEntity, 3) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        # o_his_score = torch.sum(o_score*o_att, 3) # + torch.mean(torch.norm(s_his_embedding, self.norm, 4), 3) # + (o_h_r == self.numOfRelation).float()  #batch_size*time_window*relation_sum(sample)

        #o_score = torch.sum((o_h_e_embedding - s_his_embedding)**2, 4).neg() + torch.sum(s_his_embedding**2, 4) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        s_his_embedding = ms.ops.expand_dims(ms.ops.expand_dims(s_his_embedding, 1), 1)
        o_score = ms.ops.ReduceSum()(self.Transfer_E(o_h_e_embedding)*s_his_embedding, 3)
        o_att = self.masked_softmax(o_score, o_h_e, self.numOfEntity, 2) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        o_his_score = ms.ops.ReduceSum()(o_score*o_att, 2) # + torch.mean(torch.norm(s_his_embedding, self.norm, 4), 3) # + (o_h_r == self.numOfRelation).float()  #batch_size*time_window*relation_sum(sample)

        # r_score_o = torch.sum(self.Transfer_R(p_r_embedding).unsqueeze(1).unsqueeze(1) * o_h_r_embedding,
        #                       3)  # batch_size*time_window*relation_sum(sample)
        # r_att_o = self.masked_softmax(r_score_o, o_h_r, self.numOfRelation,
        #                               2)  # batch_size*time_window*relation_sum(sample)
        # o_his_score = torch.sum(o_his_score * r_att_o, 2)  # + 1#*(time_decay == 1).float() #batch_size*time_window
        #
        # o_his_score = torch.sum(o_his_score * time_decay, 1)  # batch_size

        r_score_o = ms.ops.ReduceSum()(ms.ops.expand_dims(self.Transfer_R(p_r_embedding), 1)*o_h_r_embedding, 2) #batch_size*time_window*relation_sum(sample)
        r_att_o = self.masked_softmax(r_score_o, o_h_r, self.numOfRelation, 1) #batch_size*time_window*relation_sum(sample)
        o_his_score = ms.ops.ReduceSum()(o_his_score*r_att_o, 1)# + 1#*(time_decay == 1).float() #batch_size*time_window

        # o_his_score = ms.ops.ReduceSum()(o_his_score*time_decay, 1) #batch_size
        o_his_score = ms.ops.ReduceSum()(o_his_score.reshape([batch_size, -1]) * time_decay.reshape([batch_size, -1]), 1)
        #o_his_score = o_his_score + 0.5*(o_his_score == 0.0).float()


        # get history of head entity (with negative tail entity)
        #s_h_r_embedding = self.relation_embeddings(s_h_r) #batch_size*time_window*relation_num(sample)*hidden
        #s_h_e_embedding = self.get_time_embedding_A(s_h_e, s_h_t.unsqueeze(2).unsqueeze(2).unsqueeze(2), 4).unsqueeze(1) #batch_size*1*time_window*relation_sum(sample)*entity_num(sample)*hidden
        #ent_norm += Loss.normLoss(s_h_e_embedding, 4)

        # no_his_embedding = self.get_time_embedding_C(n_o, s_h_t.unsqueeze(1).unsqueeze(3).unsqueeze(3).unsqueeze(3),
        #                                              5)  # batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        # # ent_norm += Loss.normLoss(no_his_embedding, 5)
        # time_decay = torch.exp(-torch.abs(self.decay_rate) * torch.abs(p_t.unsqueeze(1) - s_h_t)).unsqueeze(
        #     1)  # batch_size*1*time_window
        #
        # # s_score = torch.sum((s_h_e_embedding.unsqueeze(1) - no_his_embedding)**2, 5).neg() + torch.sum(no_his_embedding**2, 5) #batch_size*ns*time_window*relation_sum(sample)*entity_num(sample)
        # s_score = torch.sum(self.Transfer_E(s_h_e_embedding).unsqueeze(1) * no_his_embedding, 5)
        # # s_att = self.masked_softmax(s_score, s_h_e.unsqueeze(1), self.numOfEntity, 4) #batch_size*ns*time_window*relation_sum(sample)*entity_num(sample)

        no_his_embedding = self.get_time_embedding_C_lowdim(n_o, ms.ops.expand_dims(ms.ops.expand_dims(s_h_t, 1), 1), 2) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        #ent_norm += Loss.normLoss(no_his_embedding, 5)
        time_decay = ms.ops.ExpandDims()(ms.ops.exp(-ms.ops.abs(self.decay_rate)*ms.ops.abs(p_t - s_h_t)), 1) #batch_size*1*time_window

        #s_score = torch.sum((s_h_e_embedding.unsqueeze(1) - no_his_embedding)**2, 5).neg() + torch.sum(no_his_embedding**2, 5) #batch_size*ns*time_window*relation_sum(sample)*entity_num(sample)
        input_1 = self.Transfer_E(s_h_e_embedding).reshape([s_h_e_embedding.shape[0], 1, -1, s_h_e_embedding.shape[3]])
        input_2 = ms.ops.expand_dims(no_his_embedding, 2)
        s_score = ms.ops.ReduceSum()(input_1*input_2, 3)
        s_score = s_score.reshape([s_score.shape[0], s_score.shape[1], s_h_e_embedding.shape[1], s_h_e_embedding.shape[2]])
        #s_att = self.masked_softmax(s_score, s_h_e.unsqueeze(1), self.numOfEntity, 4) #batch_size*ns*time_window*relation_sum(sample)*entity_num(sample)
        s_neg_score = ms.ops.ReduceSum()(s_score*ms.ops.ExpandDims()(s_att, 1), 3) # + torch.mean(torch.norm(o_his_embedding, self.norm, 4), 3) # + (s_h_r == self.numOfRelation).float() #batch_size*ns*time_window*relation_sum(sample)

        #r_score = torch.sum(self.Transfer_R(p_r_embedding).unsqueeze(1).unsqueeze(1)*s_h_r_embedding, 3) #batch_size*time_window*relation_sum(sample)
        #r_att = self.masked_softmax(r_score, s_h_r, self.numOfRelation, 2).unsqueeze(1) #batch_size*1*time_window*relation_sum(sample)
        # s_neg_score = torch.sum(s_neg_score * r_att_s.unsqueeze(1),
        #                         3)  # + 1#*(time_decay == 1).float() #batch_size*time_window
        #
        # s_neg_score = torch.sum(s_neg_score * time_decay, 2)  # batch_size*ns

        s_neg_score = ms.ops.ReduceSum()(s_neg_score*ms.ops.ExpandDims()(r_att_s, 1), 2)# + 1#*(time_decay == 1).float() #batch_size*time_window

        s_neg_score = ms.ops.ReduceSum()(s_neg_score.reshape([batch_size, -1, time_window_size])*\
                                         time_decay.reshape([batch_size, 1, -1]), 2) #batch_size*ns
        #s_neg_score = s_neg_score + 0.5*(s_neg_score == 0.0).float()


        # get history of tail entity (with negative head entity)
        #o_h_r_embedding = self.relation_embeddings(o_h_r) #batch_size*time_window*relation_num(sample)*hidden
        #o_h_e_embedding = self.get_time_embedding_A(o_h_e, o_h_t.unsqueeze(2).unsqueeze(2).unsqueeze(2), 4).unsqueeze(1) #batch_size*1*time_window*relation_sum(sample)*entity_num(sample)*hidden
        #ent_norm += Loss.normLoss(o_h_e_embedding, 4)
        # ns_his_embedding = self.get_time_embedding_C(n_s, o_h_t.unsqueeze(1).unsqueeze(3).unsqueeze(3).unsqueeze(3), 5) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        # #ent_norm += Loss.normLoss(ns_his_embedding, 5)
        # time_decay = torch.exp(-torch.abs(self.decay_rate)*torch.abs(p_t.unsqueeze(1) - o_h_t)).unsqueeze(1) #batch_size*1*time_window


        ns_his_embedding = self.get_time_embedding_C_lowdim(n_s,ms.ops.expand_dims(ms.ops.expand_dims(o_h_t, 1), 2), 2) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        #ent_norm += Loss.normLoss(ns_his_embedding, 5)
        time_decay = ms.ops.ExpandDims()(ms.ops.exp(-ms.ops.abs(self.decay_rate)*ms.ops.abs(p_t - o_h_t)), 1) #batch_size*1*time_window

        # #o_score = torch.sum((o_h_e_embedding.unsqueeze(1) - ns_his_embedding)**2, 5).neg() + torch.sum(ns_his_embedding**2, 5) #batch_size*ns*time_window*relation_sum(sample)*entity_num(sample)
        # o_score = torch.sum(self.Transfer_E(o_h_e_embedding).unsqueeze(1)*ns_his_embedding, 5)
        # #o_att = self.masked_softmax(o_score, o_h_e.unsqueeze(1), self.numOfEntity, 4) #batch_size*ns*time_window*relation_sum(sample)*entity_num(sample)
        # o_neg_score = torch.sum(o_score*o_att.unsqueeze(1), 4) # + torch.mean(torch.norm(o_his_embedding, self.norm, 4), 3) # + (s_h_r == self.numOfRelation).float() #batch_size*ns*time_window*relation_sum(sample)

        #o_score = torch.sum((o_h_e_embedding.unsqueeze(1) - ns_his_embedding)**2, 5).neg() + torch.sum(ns_his_embedding**2, 5) #batch_size*ns*time_window*relation_sum(sample)*entity_num(sample)
        input_1 = self.Transfer_E(o_h_e_embedding).reshape([o_h_e_embedding.shape[0], 1, -1, o_h_e_embedding.shape[3]])
        input_2 = ms.ops.expand_dims(ns_his_embedding, 2)
        o_score = ms.ops.ReduceSum()(input_1*input_2, 3)
        o_score = o_score.reshape([o_score.shape[0], o_score.shape[1], o_h_e_embedding.shape[1], o_h_e_embedding.shape[2]])
        #o_att = self.masked_softmax(o_score, o_h_e.unsqueeze(1), self.numOfEntity, 4) #batch_size*ns*time_window*relation_sum(sample)*entity_num(sample)
        o_neg_score = ms.ops.ReduceSum()(o_score*ms.ops.ExpandDims()(o_att, 1), 3) # + torch.mean(torch.norm(o_his_embedding, self.norm, 4), 3) # + (s_h_r == self.numOfRelation).float() #batch_size*ns*time_window*relation_sum(sample)

        #r_score = torch.sum(self.Transfer_R(p_r_embedding).unsqueeze(1).unsqueeze(1)*o_h_r_embedding, 3) #batch_size*time_window*relation_sum(sample)
        #r_att = self.masked_softmax(r_score, o_h_r, self.numOfRelation, 2).unsqueeze(1) #batch_size*1*time_window*relation_sum(sample)
        # o_neg_score = torch.sum(o_neg_score*r_att_o.unsqueeze(1), 3)# + 1#*(time_decay == 1).float() #batch_size*time_window
        #
        # o_neg_score = torch.sum(o_neg_score*time_decay, 2) #batch_size*ns

        o_neg_score = ms.ops.ReduceSum()(o_neg_score*ms.ops.ExpandDims()(r_att_o, 1), 2)# + 1#*(time_decay == 1).float() #batch_size*time_window

        o_neg_score = ms.ops.ReduceSum()(o_neg_score.reshape([batch_size, -1, time_window_size]) * \
                                         time_decay.reshape([batch_size, 1, -1]), 2)  # batch_size*ns

        #o_neg_score = o_neg_score + 0.5*(o_neg_score == 0.0).float()

        
        #get final score of pos and neg facts
        #print(p_base_score[0])
        #print(s_his_score[0])
        #print(o_his_score[0])

        p_s_score = self.trade_off*p_base_score + (1 - self.trade_off)*(s_his_score)
        p_o_score = self.trade_off*p_base_score + (1 - self.trade_off)*(o_his_score)
        ns_score = self.trade_off*ns_base_score + (1 - self.trade_off)*(o_neg_score)
        no_score = self.trade_off*no_base_score + (1 - self.trade_off)*(s_neg_score)

        
        #get loss
 #      local_loss = - torch.log(p_s_score.sigmoid() + 1e-6) \
 #                     - torch.log(p_o_score.sigmoid() + 1e-6) \
 #                     - torch.log(ns_score.neg().sigmoid() + 1e-6).sum(dim=1) \
 #                     - torch.log(no_score.neg().sigmoid() + 1e-6).sum(dim=1) \
 #
 #      local_loss = local_loss.mean()
        ms_sigmoid = nn.Sigmoid()
        p_s_score = ms_sigmoid(p_s_score)
        p_o_score = ms_sigmoid(p_o_score)
        ns_score = ms_sigmoid(ms.ops.neg(ns_score))
        no_score = ms_sigmoid(ms.ops.neg(no_score))

        local_loss = - ms.ops.log(p_s_score + 1e-6) \
                       - ms.ops.log(p_o_score + 1e-6) \
                       - ms.ops.log(ns_score + 1e-6).sum(axis = 1) \
                       - ms.ops.log(no_score + 1e-6).sum(axis = 1)

        local_loss = local_loss.mean()
        
        return local_loss# + 0.1*ent_norm


    def get_global_loss(self, p_s, p_o, p_t, n_s, n_o, s_h_e_flat, o_h_e_flat, p_s_d, p_o_d, p_t_m, p_s_o_r):

        # p_s_embedding = self.get_time_embedding_A(p_s, p_t.unsqueeze(1), 1)  # batch_size*hidden
        # p_o_embedding = self.get_time_embedding_A(p_o, p_t.unsqueeze(1), 1)  # batch_size*hidden
        #
        # n_s_embedding = self.get_time_embedding_A(n_s, p_t.unsqueeze(1).unsqueeze(1), 2)
        # n_o_embedding = self.get_time_embedding_A(n_o, p_t.unsqueeze(1).unsqueeze(1), 2)

        p_s_embedding = self.get_time_embedding_A(p_s, ms.ops.expand_dims(p_t, 1), 1) #batch_size*hidden
        p_o_embedding = self.get_time_embedding_A(p_o, ms.ops.expand_dims(p_t, 1), 1) #batch_size*hidden

        n_s_embedding = self.get_time_embedding_A(n_s, ms.ops.expand_dims(ms.ops.expand_dims(p_t, 1), 1), 2)
        n_o_embedding = self.get_time_embedding_A(n_o, ms.ops.expand_dims(ms.ops.expand_dims(p_t, 1), 1), 2)

        p_s_o_r_embedding = self.relation_embeddings(p_s_o_r) #batch_size*sample*hidden
        # r_score = torch.sigmoid(torch.sum(p_s_o_r_embedding * self.score_vector.unsqueeze(1), 2))
        # modularity = torch.sum(r_score, 1) - (p_s_d*p_o_d)/(2*p_t_m+1e-6) #batch_size

        r_score = ms.ops.Sigmoid()(ms.ops.ReduceSum()(p_s_o_r_embedding * ms.ops.expand_dims(self.score_vector, 1), 2))
        modularity = ms.ops.ReduceSum()(r_score, 1) - (p_s_d*p_o_d)/(2*p_t_m+1e-6) #batch_size

        # s_h_e_embedding = self.get_time_embedding_A(s_h_e_flat, torch.relu(p_t - 1).unsqueeze(1).unsqueeze(1), 2) #batch_size*(time_window*sample*sample)*hidden
        # s_h_e_community = torch.softmax(self.auxiliary_matrix(s_h_e_embedding), dim=2) #batch_size*(time_window*sample*sample)*community_num
        # o_h_e_embedding = self.get_time_embedding_A(o_h_e_flat, torch.relu(p_t - 1).unsqueeze(1).unsqueeze(1), 2) #batch_size*(time_window*sample*sample)*hidden
        # o_h_e_community = torch.softmax(self.auxiliary_matrix(o_h_e_embedding), dim=2) #batch_size*(time_window*sample*sample)*community_num

        ms_relu = ms.nn.ReLU()
        ms_softmax = ms.nn.Softmax(axis=2)
        s_h_e_embedding = self.get_time_embedding_A(s_h_e_flat, ms.ops.expand_dims(ms.ops.expand_dims(ms_relu(p_t - 1), 1), 1), 2) #batch_size*(time_window*sample*sample)*hidden
        s_h_e_community = ms_softmax(self.auxiliary_matrix(s_h_e_embedding)) #batch_size*(time_window*sample*sample)*community_num
        o_h_e_embedding = self.get_time_embedding_A(o_h_e_flat, ms.ops.expand_dims(ms.ops.expand_dims(ms_relu(p_t - 1), 1), 1), 2) #batch_size*(time_window*sample*sample)*hidden
        o_h_e_community = ms_softmax(self.auxiliary_matrix(o_h_e_embedding)) #batch_size*(time_window*sample*sample)*community_num

        # p_s_his_embedding = self.get_time_embedding_A(p_s, torch.relu(p_t - 1).unsqueeze(1), 1).unsqueeze(
        #     1)  # batch_size*1*hidden
        # s_his_community = torch.softmax(self.auxiliary_matrix(p_s_his_embedding), dim=2)  # batch_size*1*community_num
        # p_o_his_embedding = self.get_time_embedding_A(p_o, torch.relu(p_t - 1).unsqueeze(1), 1).unsqueeze(
        #     1)  # batch_size*1*hidden
        # o_his_community = torch.softmax(self.auxiliary_matrix(p_o_his_embedding), dim=2)  # batch_size*1*community_num

        p_s_his_embedding = ms.ops.expand_dims(self.get_time_embedding_A(p_s, ms.ops.expand_dims(ms_relu(p_t - 1), 1), 1), 1) #batch_size*1*hidden
        s_his_community = ms_softmax(self.auxiliary_matrix(p_s_his_embedding)) #batch_size*1*community_num
        p_o_his_embedding = ms.ops.expand_dims(self.get_time_embedding_A(p_o, ms.ops.expand_dims(ms_relu(p_t - 1), 1), 1), 1) #batch_size*1*hidden
        o_his_community = ms_softmax(self.auxiliary_matrix(p_o_his_embedding)) #batch_size*1*community_num

        # s_mask = ((s_his_community >= 0.2).float() * (s_h_e_community >= 0.2).float()).sum(2)
        # s_mask = (s_mask != 0).float()
        # s_C_embedding = torch.mean(s_h_e_embedding * s_mask.unsqueeze(2), 1)
        #
        # o_mask = ((o_his_community >= 0.2).float() * (o_h_e_community >= 0.2).float()).sum(2)
        # o_mask = (o_mask != 0).float()
        # o_C_embedding = torch.mean(o_h_e_embedding * o_mask.unsqueeze(2), 1)

        ms_cast = ms.ops.Cast()
        ms_mean = ms.ops.ReduceMean()
        s_mask = (ms_cast(s_his_community >= 0.2, ms.float32) * ms_cast(s_h_e_community >= 0.2, ms.float32)).sum(axis=2)
        s_mask = ms_cast(s_mask != 0, ms.float32)
        s_C_embedding = ms_mean(s_h_e_embedding*ms.ops.expand_dims(s_mask, 2), axis=1)

        o_mask = (ms_cast(o_his_community >= 0.2, ms.float32) * ms_cast(o_h_e_community >= 0.2, ms.float32)).sum(axis=2)
        o_mask = ms_cast(o_mask != 0, ms.float32)
        o_C_embedding = ms_mean(o_h_e_embedding*ms.ops.expand_dims(o_mask, 2), axis=1)

        # p_s_community = torch.softmax(self.auxiliary_matrix(p_s_embedding + s_C_embedding),
        #                               dim=1)  # batch_size*community_num
        # p_s_community = (self.numOfEntity ** 0.5 * p_s_community ** 0.5) / (
        #     (p_s_community ** 0.5).sum(dim=1).sum(dim=0))
        # p_o_community = torch.softmax(self.auxiliary_matrix(p_o_embedding + o_C_embedding),
        #                               dim=1)  # batch_size*community_num
        # p_o_community = (self.numOfEntity ** 0.5 * p_o_community ** 0.5) / (
        #     (p_o_community ** 0.5).sum(dim=1).sum(dim=0))
        ms_softmax = ms.nn.Softmax(axis=1)
        p_s_community = ms_softmax(self.auxiliary_matrix(p_s_embedding + s_C_embedding)) #batch_size*community_num
        p_s_community = (self.numOfEntity**0.5 * p_s_community**0.5)/((p_s_community**0.5).sum(axis=1).sum(axis=0))
        p_o_community = ms_softmax(self.auxiliary_matrix(p_o_embedding + o_C_embedding)) #batch_size*community_num
        p_o_community = (self.numOfEntity**0.5 * p_o_community**0.5)/((p_o_community**0.5).sum(axis=1).sum(axis=0))

        global_loss = - ms_mean(ms.ops.ReduceSum()(p_s_community*p_o_community, 1)*modularity, axis=0)
        
        # norm_loss = 0
        # # for W in self.auxiliary_matrix.parameters():
        # #     norm_loss += Loss.F_norm(W)
        # for W in self.auxiliary_matrix.get_parameters():
        #     norm_loss += Loss.F_norm(W)

        # return global_loss + 0.01*norm_loss
        return global_loss

    def get_co_loss(self):

        return 0


    def validate(self,p_s, p_r, p_o, p_t, \
                s_h_r, s_h_e, s_h_t, \
                o_h_r, o_h_e, o_h_t, \
                TrainData):
        MRR = 0.0
        H1 = 0.0
        H3 = 0.0
        H5 = 0.0
        H10 = 0.0
        # get base intensity of candidate facts
        p_s_embedding = self.get_time_embedding_A(p_s, ms.ops.expand_dims(p_t, 1), 1)# batch_size*hidden
        p_o_embedding = self.get_time_embedding_A(p_o, ms.ops.expand_dims(p_t, 1), 1)
        all_embedding = self.get_time_embedding_D(ms.ops.expand_dims(ms.ops.expand_dims(p_t, 1), 1), 2)# batch_size*numOfEntity*hidden

        p_r_embedding = self.relation_embeddings(p_r)
        '''
        base_score_target = torch.sum((p_s_embedding + p_r_embedding - p_o_embedding)**2, 1).unsqueeze(1).neg() # batch_size*1
        base_score_head = torch.sum((all_embedding + p_r_embedding.unsqueeze(1) - p_o_embedding.unsqueeze(1))**2, 2).neg() 
        base_score_tail = torch.sum((p_s_embedding.unsqueeze(1) + p_r_embedding.unsqueeze(1) - all_embedding)**2, 2).neg() # batch_size*numOfEntity
        '''
        '''
        p_base_emb = p_s_embedding * p_r_embedding * p_o_embedding
        base_score_target = torch.sum(p_base_emb, 1)#/torch.norm(p_base_emb, 2, 1)
        ns_base_emb = all_embedding * p_r_embedding.unsqueeze(1) * p_o_embedding.unsqueeze(1)#batch_size*ns
        base_score_head = torch.sum(ns_base_emb, 2)#/torch.norm(ns_base_emb, 2, 2)
        no_base_emb = p_s_embedding.unsqueeze(1) * p_r_embedding.unsqueeze(1) * all_embedding
        base_score_tail = torch.sum(no_base_emb, 2)#/torch.norm(no_base_emb, 2, 2)
        '''

        # base_score_target = (self.Transfer_SH(p_s_embedding + p_r_embedding))  # batch_size
        # base_score_target = torch.sum(p_o_embedding * base_score_target, 1)  # .neg()
        # base_score_head = (self.Transfer_SH(all_embedding + p_r_embedding.unsqueeze(1)))  # batch_size*ns
        # base_score_head = torch.sum(p_o_embedding.unsqueeze(1) * base_score_head, 2)  # .neg()
        # base_score_tail = (self.Transfer_SH(p_s_embedding + p_r_embedding))
        # base_score_tail = torch.sum(all_embedding * base_score_tail.unsqueeze(1), 2)  # .neg()

        base_score_target = (self.Transfer_SH(p_s_embedding + p_r_embedding)) #batch_size
        base_score_target = ms.ops.ReduceSum()(p_o_embedding*base_score_target, axis=1)#.neg()
        base_score_head = (self.Transfer_SH(all_embedding + ms.ops.expand_dims(p_r_embedding, 1))) #batch_size*ns
        base_score_head = ms.ops.ReduceSum()(ms.ops.expand_dims(p_o_embedding, 1)*base_score_head, axis=2)#.neg()
        base_score_tail = (self.Transfer_SH(p_s_embedding + p_r_embedding))
        base_score_tail = ms.ops.ReduceSum()(all_embedding*ms.ops.expand_dims(base_score_tail, 1), axis=2)#.neg()

        batch_size = o_h_r.shape[0]
        time_window_size = o_h_r.shape[1]

        o_h_e = o_h_e.reshape([-1, o_h_e.shape[2], o_h_e.shape[3]])
        o_h_r = o_h_r.reshape([-1, o_h_r.shape[2]])
        o_h_t = o_h_t.reshape([-1])

        s_h_e = s_h_e.reshape([-1, s_h_e.shape[2], s_h_e.shape[3]])
        s_h_r = s_h_r.reshape([-1, s_h_r.shape[2]])
        s_h_t = s_h_t.reshape([-1])

        p_o_source = p_o
        p_t_source = p_t
        p_s_source = p_s
        p_r_source = p_r

        p_o = p_o.repeat(time_window_size, axis=0)
        p_t = p_t.repeat(time_window_size, axis=0)
        p_s = p_s.repeat(time_window_size, axis=0)
        p_r = p_r.repeat(time_window_size, axis=0)

        p_r_embedding = p_r_embedding.repeat(time_window_size, axis=0)
        # get history of head entity

        # s_h_r_embedding = self.relation_embeddings(s_h_r)  # batch_size*time_window*relation_num(sample)*hidden
        # s_h_e_embedding = self.get_time_embedding_A(s_h_e, s_h_t.unsqueeze(2).unsqueeze(2).unsqueeze(2),
        #                                             4)  # batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        # o_his_embedding = self.get_time_embedding_B(p_o, s_h_t.unsqueeze(2).unsqueeze(2).unsqueeze(2),
        #                                             4)  # batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        # time_decay = torch.exp(
        #     -torch.abs(self.decay_rate) * torch.abs(p_t.unsqueeze(1) - s_h_t))  # batch_size*time_window
        s_h_r_embedding = self.relation_embeddings(s_h_r) #batch_size*time_window*relation_num(sample)*hidden
        s_h_e_embedding = self.get_time_embedding_A(s_h_e, ms.ops.expand_dims(ms.ops.expand_dims(
            ms.ops.expand_dims(s_h_t, 1), 1), 1), 3) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        o_his_embedding = self.get_time_embedding_B_lowdim(p_o, ms.ops.expand_dims(s_h_t, 1), 1) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        time_decay = ms.ops.exp(-ms.ops.abs(self.decay_rate)*ms.ops.abs(p_t - s_h_t)) #batch_size*time_window

        # #s_score = torch.sum((s_h_e_embedding - o_his_embedding)**2, 4).neg() + torch.sum(o_his_embedding**2, 4) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        # s_score = torch.sum(self.Transfer_E(s_h_e_embedding)*o_his_embedding, 4)
        # s_att = self.masked_softmax(s_score, s_h_e, self.numOfEntity, 3) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        # s_his_score = torch.sum(s_score*s_att, 3)# + torch.mean(torch.norm(o_his_embedding, self.norm, 4), 3) # + (s_h_r == self.numOfRelation).float() #batch_size*time_window*relation_sum(sample)

        #s_score = torch.sum((s_h_e_embedding - o_his_embedding)**2, 4).neg() + torch.sum(o_his_embedding**2, 4) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        o_his_embedding = ms.ops.expand_dims(ms.ops.expand_dims(o_his_embedding, 1), 1)
        s_score = ms.ops.ReduceSum()(self.Transfer_E(s_h_e_embedding)*o_his_embedding, 3)
        s_att = self.masked_softmax(s_score, s_h_e, self.numOfEntity, 2) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        s_his_score = ms.ops.ReduceSum()(s_score*s_att, 2)# + torch.mean(torch.norm(o_his_embedding, self.norm, 4), 3) # + (s_h_r == self.numOfRelation).float() #batch_size*time_window*relation_sum(sample)

        # r_score = torch.sum(self.Transfer_R(p_r_embedding).unsqueeze(1).unsqueeze(1) * s_h_r_embedding,
        #                     3)  # batch_size*time_window*relation_sum(sample)
        # r_att_s = self.masked_softmax(r_score, s_h_r, self.numOfRelation,
        #                               2)  # batch_size*time_window*relation_sum(sample)
        # s_his_score = torch.sum(s_his_score * r_att_s, 2)  # + 1#*(time_decay == 1).float() #batch_size*time_window
        #
        # s_his_score = torch.sum(s_his_score * time_decay, 1)  # batch_size
        # # s_his_score = s_his_score + 0.5*(s_his_score == 0.0).float()

        r_score = ms.ops.ReduceSum()(ms.ops.expand_dims(self.Transfer_R(p_r_embedding), 1)*s_h_r_embedding, 2) #batch_size*time_window*relation_sum(sample)
        r_att_s = self.masked_softmax(r_score, s_h_r, self.numOfRelation, 1) #batch_size*time_window*relation_sum(sample)
        s_his_score = ms.ops.ReduceSum()(s_his_score*r_att_s, 1)# + 1#*(time_decay == 1).float() #batch_size*time_window

        s_his_score = ms.ops.ReduceSum()(s_his_score.reshape([batch_size, -1])*time_decay.reshape([batch_size, -1]), 1) #batch_size
        #s_his_score = s_his_score + 0.5*(s_his_score == 0.0).float()


        # get history of tail entity
        o_h_r_embedding = self.relation_embeddings(o_h_r) #batch_size*time_window*relation_num(sample)*hidden
        o_h_e_embedding = self.get_time_embedding_A(o_h_e, ms.ops.expand_dims(ms.ops.expand_dims(
            ms.ops.expand_dims(o_h_t, 1), 1), 1), 3) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        s_his_embedding = self.get_time_embedding_B_lowdim(p_s, ms.ops.expand_dims(o_h_t, 1), 1) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        time_decay = ms.ops.exp(-ms.ops.abs(self.decay_rate)*ms.ops.abs(p_t - o_h_t)) #batch_size*time_window

        # #o_score = torch.sum((o_h_e_embedding - s_his_embedding)**2, 4).neg() + torch.sum(s_his_embedding**2, 4) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        # o_score = torch.sum(self.Transfer_E(o_h_e_embedding)*s_his_embedding, 4)
        # o_att = self.masked_softmax(o_score, o_h_e, self.numOfEntity, 3)  #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        # o_his_score = torch.sum(o_score*o_att, 3)# + torch.mean(torch.norm(s_his_embedding, self.norm, 4), 3) # + (o_h_r == self.numOfRelation).float() #batch_size*time_window*relation_sum(sample)

        #o_score = torch.sum((o_h_e_embedding - s_his_embedding)**2, 4).neg() + torch.sum(s_his_embedding**2, 4) #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        s_his_embedding = ms.ops.expand_dims(ms.ops.expand_dims(s_his_embedding, 1), 1)
        o_score = ms.ops.ReduceSum()(self.Transfer_E(o_h_e_embedding)*s_his_embedding, 3)
        o_att = self.masked_softmax(o_score, o_h_e, self.numOfEntity, 2)  #batch_size*time_window*relation_sum(sample)*entity_num(sample)
        o_his_score = ms.ops.ReduceSum()(o_score*o_att, 2)# + torch.mean(torch.norm(s_his_embedding, self.norm, 4), 3) # + (o_h_r == self.numOfRelation).float() #batch_size*time_window*relation_sum(sample)

        r_score = ms.ops.ReduceSum()(ms.ops.expand_dims(self.Transfer_R(p_r_embedding), 1)*o_h_r_embedding, 2) #batch_size*time_window*relation_sum(sample)
        r_att_o = self.masked_softmax(r_score, o_h_r, self.numOfRelation, 1) #batch_size*time_window*relation_sum(sample)
        o_his_score = ms.ops.ReduceSum()(o_his_score*r_att_o, 1)# + 1#*(time_decay == 1).float() #batch_size*time_window

        o_his_score = ms.ops.ReduceSum()(o_his_score.reshape([batch_size, -1])*time_decay.reshape([batch_size, -1]), 1) #batch_size
        #o_his_score = o_his_score + 0.5*(o_his_score == 0.0).float()
        
        # get history of head entity (with negative tail entity)
        #s_h_r_embedding = self.relation_embeddings(s_h_r) #batch_size*time_window*relation_num(sample)*hidden
        #s_h_e_embedding = self.get_time_embedding_A(s_h_e, s_h_t.unsqueeze(2).unsqueeze(2).unsqueeze(2), 4).unsqueeze(1) #batch_size*1*time_window*relation_sum(sample)*entity_num(sample)*hidden
        no_his_embedding = self.get_time_embedding_E_lowdim(ms.ops.expand_dims(ms.ops.expand_dims(s_h_t, 1), 1), 3) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        time_decay = ms.ops.expand_dims(ms.ops.exp(-ms.ops.abs(self.decay_rate)*ms.ops.abs(p_t - s_h_t)), 1) #batch_size*1*time_window

        #s_score = torch.sum((s_h_e_embedding.unsqueeze(1) - no_his_embedding)**2, 5).neg() + torch.sum(no_his_embedding**2, 5) #batch_size*ns*time_window*relation_sum(sample)*entity_num(sample)
        input_1 = ms.ops.expand_dims(s_h_e_embedding.reshape([s_h_e_embedding.shape[0], -1, s_h_e_embedding.shape[3]]), 1)
        input_2 = ms.ops.expand_dims(no_his_embedding, 2)
        s_score =  ms.ops.ReduceSum()(self.Transfer_E(input_1)*input_2, 3)
        s_score = s_score.reshape([s_score.shape[0], s_score.shape[1], s_h_e_embedding.shape[1], s_h_e_embedding.shape[2]])
        #s_att = self.masked_softmax(s_score, s_h_e.unsqueeze(1), self.numOfEntity, 4) #batch_size*ns*time_window*relation_sum(sample)*entity_num(sample)
        s_neg_score = ms.ops.ReduceSum()(s_score*ms.ops.expand_dims(s_att, 1), 3) # + torch.mean(torch.norm(o_his_embedding, self.norm, 4), 3) # + (s_h_r == self.numOfRelation).float() #batch_size*ns*time_window*relation_sum(sample)

        #r_score = torch.sum(self.Transfer_R(p_r_embedding).unsqueeze(1).unsqueeze(1)*s_h_r_embedding, 3) #batch_size*time_window*relation_sum(sample)
        #r_att = self.masked_softmax(r_score, s_h_r, self.numOfRelation, 2).unsqueeze(1) #batch_size*1*time_window*relation_sum(sample)
        s_neg_score = ms.ops.ReduceSum()(s_neg_score*ms.ops.expand_dims(r_att_s, 1), 2)# + 1#*(time_decay == 1).float() #batch_size*time_window

        s_neg_score = ms.ops.ReduceSum()(s_neg_score.reshape([batch_size, -1, time_window_size])*\
                                         time_decay.reshape([batch_size, 1, -1]), 2) #batch_size*ns
        #s_neg_score = s_neg_score + 0.5*(s_neg_score == 0.0).float()



        # get history of tail entity (with negative head entity)
        #o_h_r_embedding = self.relation_embeddings(o_h_r) #batch_size*time_window*relation_num(sample)*hidden
        #o_h_e_embedding = self.get_time_embedding_A(o_h_e, o_h_t.unsqueeze(2).unsqueeze(2).unsqueeze(2), 4).unsqueeze(1) #batch_size*1*time_window*relation_sum(sample)*entity_num(sample)*hidden
        ns_his_embedding = self.get_time_embedding_E_lowdim(ms.ops.expand_dims(ms.ops.expand_dims(o_h_t, 1), 1), 3) #batch_size*time_window*relation_sum(sample)*entity_num(sample)*hidden
        time_decay = ms.ops.expand_dims(ms.ops.exp(-ms.ops.abs(self.decay_rate)*ms.ops.abs(p_t - o_h_t)), 1) #batch_size*1*time_window

        #o_score = torch.sum((o_h_e_embedding.unsqueeze(1) - ns_his_embedding)**2, 5).neg() + torch.sum(ns_his_embedding**2, 5) #batch_size*ns*time_window*relation_sum(sample)*entity_num(sample)
        # o_score = torch.sum(self.Transfer_E(o_h_e_embedding).unsqueeze(1) * ns_his_embedding, 5)
        input_1 = ms.ops.expand_dims(o_h_e_embedding.reshape([o_h_e_embedding.shape[0], -1, o_h_e_embedding.shape[3]]), 1)
        input_2 = ms.ops.expand_dims(ns_his_embedding, 2)
        o_score = ms.ops.ReduceSum()(self.Transfer_E(input_1)*input_2, 3)
        #o_att = self.masked_softmax(o_score, o_h_e.unsqueeze(1), self.numOfEntity, 4) #batch_size*ns*time_window*relation_sum(sample)*entity_num(sample)
        o_score = o_score.reshape([o_score.shape[0], o_score.shape[1], o_h_e_embedding.shape[2], o_h_e_embedding.shape[2]])
        o_neg_score = ms.ops.ReduceSum()(o_score*ms.ops.expand_dims(o_att, 1), 3) # + torch.mean(torch.norm(o_his_embedding, self.norm, 4), 3) # + (s_h_r == self.numOfRelation).float() #batch_size*ns*time_window*relation_sum(sample)

        #r_score = torch.sum(self.Transfer_R(p_r_embedding).unsqueeze(1).unsqueeze(1)*o_h_r_embedding, 3) #batch_size*time_window*relation_sum(sample)
        #r_att = self.masked_softmax(r_score, o_h_r, self.numOfRelation, 2).unsqueeze(1) #batch_size*1*time_window*relation_sum(sample)
        o_neg_score = ms.ops.ReduceSum()(o_neg_score*ms.ops.expand_dims(r_att_o, 1), 2)# + 1#*(time_decay == 1).float() #batch_size*time_window

        o_neg_score = ms.ops.ReduceSum()(o_neg_score.reshape([batch_size, -1, time_window_size])*\
                                time_decay.reshape([batch_size, 1, -1]), 2) #batch_size*ns
        #o_neg_score = o_neg_score + 0.5*(o_neg_score == 0.0).float()
        #print(o_neg_score.size())
        
        for i in range(len(p_s_source)):
            s_i = int(p_s_source[i])
            r_i = int(p_r_source[i])
            o_i = int(p_o_source[i])
            t_i = int(p_t_source[i])

            # get final score pos and neg fact
            #target_s_score = self.trade_off*base_score_target[i] + (1 - self.trade_off)*(s_his_score[i])
            #target_o_score = self.trade_off*base_score_target[i] + (1 - self.trade_off)*(o_his_score[i])

            tmp_head_score = (self.trade_off * base_score_head[i] + (1 - self.trade_off) * (o_neg_score[i])).squeeze(0)
            tmp_tail_score = (self.trade_off * base_score_tail[i] + (1 - self.trade_off) * (s_neg_score[i])).squeeze(0)


            # get rank
            tmp_head = (- tmp_head_score[s_i] + tmp_head_score)
            tmp_tail = (- tmp_tail_score[o_i] + tmp_tail_score)
            
            if s_i in TrainData["er2e"].keys() and r_i in TrainData["er2e"][s_i].keys() and t_i in TrainData["er2e"][s_i][r_i].keys():
                tail_list = list(set(TrainData["er2e"][s_i][r_i][t_i]))
                tmp_tail[tail_list] = 0
            if o_i in TrainData["er2e"].keys() and r_i in TrainData["er2e"][o_i].keys() and t_i in TrainData["er2e"][o_i][r_i].keys():
                head_list = list(set(TrainData["er2e"][o_i][r_i][t_i]))
                tmp_head[head_list] = 0

            # wrongHead = torch.nonzero(nn.functional.relu(tmp_head))
            # wrongTail = torch.nonzero(nn.functional.relu(tmp_tail))

            wrongHead=ms.ops.count_nonzero(ms.nn.ReLU()(tmp_head))
            wrongTail=ms.ops.count_nonzero(ms.nn.ReLU()(tmp_tail))

            # Rank_H = wrongHead.size()[0] + 1
            # Rank_T = wrongTail.size()[0] + 1
            Rank_H=wrongHead+1
            Rank_T=wrongTail+1

            MRR += 1./Rank_H+ 1./Rank_T
            
            if Rank_H<=1:
                H1+=1
            if Rank_T<=1:
                H1+=1

            if Rank_H<=3:
                H3+=1
            if Rank_T<=3:
                H3+=1

            if Rank_H<=5:
                H5+=1
            if Rank_T<=5:
                H5+=1

            if Rank_H<=10:
                H10+=1
            if Rank_T<=10:
                H10+=1

        return MRR, H1, H3, H5, H10