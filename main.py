# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 19:53:49 20

Ce fichier définit une variable mais aussi un jeu de variable.
- Une variable peut être associée ou non à un code, une traduction de 
ses modalités en valeurs explicites mais plus longues.
- Par extension, un jeu de données à une liste de variables mais aussi
un dictionnaire des codes.

Le programme permet de comparer deux variables et deux jeux de données.

TODO: traduire un jeu dans une base, créer des modalité unifiées
etc.

@author: Alexis
"""

# Note: on a deux types de variable, celles avec des valeurs directements
# et celle avec un code pour les valeurs


def _no_dup(liste):
    for i in range(len(liste)):
        if liste[i] in liste[i + 1:]:
            return False
    return True
#    return len(unique(liste)) == len(liste)
    
def _compare(list1, list2):
        set1 = set(list1)
        set2 = set(list2)    
        removed = set1 - set2
        added = set2 - set1
        return added, removed        
    

class Var(object):
    ''' definit une variable simple
        elle a des modalités
    '''
    def __init__(self, name, modalites):
        self.name = name
        self.modalites = modalites
        test = modalites[0]
        if isinstance(test, str):
            self.type = type(test)
        assert all([isinstance(x, self.type) for x in modalites[1:]])
        assert _no_dup(modalites)
        if self.type is tuple:
            assert all(len(x) == 2 for x in modalites)
            
    def compare(self, var2, print_option=False):
        assert isinstance(var2, Var)
        assert var2.type == self.type
        added, removed = _compare(self.modalites, var2.modalites)
        if print_option:
            if removed:
                print('\t les modalités ', removed, ' ne sont plus dans ', var2.name)
            else:
                print("\t aucune modalité n'a disparu")
            if added:
                print('\t les modalités ', added, ' sont apparues ', var2.name)
            else:
                print("\t aucune modalité n'a été ajoutée")
        return added, removed
        
            
class VarDico(Var):
    ''' definit des variables dont les modalités sont codées '''
    def __init__(self, name, modalites, explications):
        Var.__init__(self, name, modalites)
        self.explications = explications
        assert all([x in explications.keys() for x in modalites])
    
    def compare(self, var2, print_option=False):
        assert isinstance(var2, Var)
        diff_modalites = Var.compare(self, var2, print_option)
        if isinstance(var2, VarDico):
            # compare la présence des modalités
            diff_code = _compare(self.explications.keys(),
                                 var2.explications.keys())
            # TODO: améliorer ce print
            print diff_code
            ## comparer les valeurs des modalités
            new_explic = var2.explications
            for code, explic in self.explications.iteritems():
                if code not in new_explic:
                    print "le code " + code + " is not in " + var2.name
                else:
                    if new_explic[code] != explic:
                        print ("Pour " + var2.name + ", le code " + str(code) + 
                                " vaut " + new_explic[code] + ' et non ' + explic)


class DicoDeCodes(object):
    
    def __init__(self, name, dictionnaire, explications = None):
        self.name = name
        dic = dictionnaire
        assert isinstance(dic, dict)
        assert _no_dup(dic.keys())
        if explications is not None:
            assert isinstance(explications, dict)
            assert _no_dup(explications.keys())
        self.dico = dic
        self.dic_var = dict()
        for name, var in dic.iteritems():
            if name in explications:
                self.dic_var[name] = VarDico(name, var, explications[name])
            else:
                self.dic_var[name] = Var(name, var)
        self.explications = explications


    def compare_variables(self, dic2, print_option=False):
        ''' renvoie un dictionnaire avec les changements de variables entre
            les deux dictionnaires.
            dic2 est comparé à la référence self
        '''
        assert isinstance(dic2, DicoDeCodes)
        var_self = set(self.dico.keys())
        var_dic2 = set(dic2.dico.keys())
        removed = var_self - var_dic2
        added = var_dic2 - var_self
        if print_option:
            if removed:
                print('les variables ', removed, ' ne sont plus dans ', dic2.name)
            else:
                print("aucune variable n'a disparu")
            if added:
                print('les variables ', added, ' ont apparus ', dic2.name)
            else:
                print("aucune variable n'a été ajoutée")
        
        
    def compare(self, dic2, print_option=False):
        ''' renvoie un dictionnaire avec les changements entre
            les deux dictionnaires.
            dic2 est comparé à la référence self
        '''
        assert isinstance(dic2, DicoDeCodes)
        new_dico = dic2.dic_var
        for name, var in self.dic_var.iteritems():
            print "\n"
            print 'la variabel' + var.name
            if name not in new_dico:
                print "le code " + name + " n'est pas présent"
            else:
                var2 = new_dico[name]
                var.compare(var2, print_option)
            
    
    
# definition table1
tab1 = dict(
            var1 = [('mod1', 'name1'), ('mod2', 'name2'), ('mod3', 'name3')],
            var2 = [('mod1', 'name1'), ('mod2', 'name2'), ('mod3', 'name3')],
            var3 = [('mod1', 'name1'), ('mod2', 'name2'), ('mod3', 'name3')],
            )
            
tab2 = dict(
            var1 = [('mod1', 'name1'), ('mod2', 'name2'), ('mod3', 'name3')],
            var2 = [('mod1', 'name1'), ('mod2', 'name2')],
            var3 = [('mod1', 'name1'), ('mod2', 'name2'), ('mod3', 'name3'),
                    ('mod4', 'name4')],
            )

tab1 = dict(
            var1 = ['mod1', 'mod2', 'mod3'],
            var2 = ['mod1', 'mod2', 'mod3'],
            var3 = ['mod1', 'mod2', 'mod3'],
            )
            
tab2 = dict(
            var1 = ['mod1', 'mod2', 'mod3'],
            var2 = ['mod1', 'mod2'],
            var3 = ['mod1', 'mod2', 'mod3', 'mod4'],
            )
            
explic1 = dict(
               mod1 = "name1",
               mod2 = "name2",
               mod3 = "name3",
               )

explic2 = dict(
               mod1 = "name1",
               mod2 = "name2",
               mod3 = "Name3",
               mod4 = "name4",
               )

#for var in tab2: 
#    v1 = Var(var, tab1[var])
#    v2 = Var(var, tab2[var])
#    v1.compare(v2, print_option=True)
#


#for var in tab2: 
#    v1 = VarDico(var, tab1[var], explic1)
#    v2 = VarDico(var, tab2[var], explic2)
#    v1.compare(v2, print_option=True)
explications1 = dict(var1 = explic1, var2= explic1)
explications2 = dict(var1 = explic2, var2= explic2)
dic1 = DicoDeCodes('init', tab1, explications1)
dic2 = DicoDeCodes('new', tab2, explications2)
    
dic1.compare(dic2, True)
    
#def check_dico_des_codes(dic):
#    ''' vérifie si dic a bien un forme de dico des codes '''
#    assert isinstance(dic, dict)
#    assert _no_dup(dic.keys())
#    for list_values in dic.values():
#        assert all([isinstance(value, tuple) for value in list_values])
#        assert all([len(value) == 2 for value in list_values])        
#        assert _no_dup(values)
        

    