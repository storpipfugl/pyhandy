from scipy.integrate import ode
import matplotlib.pyplot as plt


def state(_, y, commoner_birth_rate, elite_birth_rate, commoner_death_rate,
        elite_death_rate, nature_capacity, nature_regeneration, depletion, 
        commoner_comsumption, elite_consumption):
    return [
        commoner_birth_rate * y[0] - commoner_death_rate * y[0], 
        elite_birth_rate * y[1] - elite_death_rate * y[1],
        nature_regeneration * y[2] * (nature_capacity - y[2]) - depletion * y[0] * y[2],
        depletion * y[0] * y[2] - commoner_comsumption - elite_consumption 
    ]

class Society(object):

    def __init__(self, min_required_consumption, output_division, salary,
        commoner_population, elite_population, nature, nature_regeneration, 
        nature_capacity, depletion, wealth,
        commoner_birth_rate, elite_birth_rate,
        normal_death_rate, famine_death_rate, year):

        self.min_required_consumption = float(min_required_consumption)
        self.output_division = float(output_division)
        self.salary = float(salary)
        self.commoner_population = float(commoner_population)
        self.elite_population = float(elite_population)
        self.nature = float(nature)
        self.nature_regeneration = float(nature_regeneration)
        self.nature_capacity = float(nature_capacity)
        self.depletion = float(depletion)
        self.wealth = float(wealth)
        self.commoner_birth_rate = float(commoner_birth_rate)
        self.elite_birth_rate = float(elite_birth_rate)
        self.normal_death_rate = float(normal_death_rate)
        self.famine_death_rate = float(famine_death_rate)
        self.year = int(year)

        self._integrator = ode(state).set_integrator('dopri5')
        self._integrator.set_initial_value((self.commoner_population,
            self.elite_population, self.nature, self.wealth), self.year)

    @property
    def wealth_threshold(self):
        return (self.min_required_consumption * (self.commoner_population
            + self.output_division * self.elite_population))

    @property
    def commoner_comsumption(self):
        return min(1, self.wealth / self.wealth_threshold) \
            * self.salary * self.commoner_population

    @property
    def elite_consumption(self):
        if self.elite_population == 0:
            return 0
        else:
            return min(1, self.wealth / self.wealth_threshold) \
                * self.output_division * self.salary * self.elite_population

    @property
    def commoner_death_rate(self):
        return (self.normal_death_rate 
            + max(0, 1 - self.commoner_comsumption / (self.salary * self.commoner_population))
            * (self.famine_death_rate - self.normal_death_rate))
        
    @property
    def elite_death_rate(self):
        if self.elite_population == 0:
            return 0
        else:
            return (self.normal_death_rate 
                + max(0, 1 - self.elite_consumption / (self.salary * self.elite_population))
                * (self.famine_death_rate - self.normal_death_rate))

    def next(self):
        self._integrator.set_f_params(self.commoner_birth_rate,
            self.elite_birth_rate, self.commoner_death_rate,
            self.elite_death_rate, self.nature_capacity, self.nature_regeneration, self.depletion, 
            self.commoner_comsumption, self.elite_consumption)

        self._integrator.integrate(self._integrator.t + 1)
        (self.commoner_population, self.elite_population, self.nature, 
            self.wealth) = self._integrator.y
        self.year = self._integrator.t

        return [self.year, self.commoner_population, self.elite_population, self.nature, 
            self.wealth]
    
    def evolve(self, years=1000):
        time = []
        commoner_population = []
        elite_population = []
        nature = []
        wealth = []

        for year in range(self.year, years):
            next_y, next_cp, next_ep, next_n, next_w = self.next()
            time.append(next_y)
            commoner_population.append(next_cp)
            elite_population.append(next_ep)
            nature.append(next_n)
            wealth.append(next_w)

        return time, commoner_population, elite_population, nature, wealth


socity_types = { 'egalitarian': { 'soft': (5e-3, 1, 5e-4, 100, 0, 100, 1e-2,
                                           100, 6.67e-6, 0, 3e-2, 3e-2, 1e-2,
                                           7e-2, 0),
                                  'oscillatory': (5e-3, 1, 5e-4, 100, 0, 100, 1e-2,
                                           100, 1.67e-5, 0, 3e-2, 3e-2, 1e-2,
                                           7e-2, 0),
                                  'cyclic': (5e-3, 1, 5e-4, 100, 0, 100, 1e-2,
                                           100, 2.67e-5, 0, 3e-2, 3e-2, 1e-2,
                                           7e-2, 0),
                                  'collapse': (5e-3, 1, 5e-4, 100, 0, 100, 1e-2,
                                           100, 3.67e-5, 0, 3e-2, 3e-2, 1e-2,
                                           7e-2, 0)
                                },
                'equitable': { 'soft': (5e-3, 1, 5e-4, 100, 25, 100, 1e-2,
                                           100, 8.33e-6, 0, 3e-2, 3e-2, 1e-2,
                                           7e-2, 0),
                                  'oscillatory': (5e-3, 1, 5e-4, 100, 25, 100, 1e-2,
                                           100, 2.2e-5, 0, 3e-2, 3e-2, 1e-2,
                                           7e-2, 0),
                                  'cyclic': (5e-3, 1, 5e-4, 100, 25, 100, 1e-2,
                                           100, 3.0e-5, 0, 3e-2, 3e-2, 1e-2,
                                           7e-2, 0),
                                  'collapse': (5e-3, 1, 5e-4, 100, 25, 100, 1e-2,
                                           100, 3.0e-5, 0, 3e-2, 3e-2, 1e-2,
                                           7e-2, 0),
                                  'inverse': (5e-3, 1, 5e-4, 100, 600, 100, 1e-2,
                                           100, 4.33e-5, 0, 3e-2, 3e-2, 1e-2,
                                           7e-2, 0)
                                },
                'unequal': { 'type-l': (5e-3, 100, 5e-4, 100, 1.0e-3, 100, 1e-2,
                                           100, 6.67e-6, 0, 3e-2, 3e-2, 1e-2,
                                           7e-2, 0),
                                  'collapse': (5e-3, 100, 5e-4, 100, 0.2, 100, 1e-2,
                                           100, 1.0e-4, 0, 3e-2, 3e-2, 1e-2,
                                           7e-2, 0),
                                  'soft': (5e-3, 10, 5e-4, 10000, 3000, 100, 1e-2,
                                           100, 6.35e-6, 0, 6.5e-2, 2.0e-2, 1e-2,
                                           7e-2, 0),
                                  'oscillatory': (5e-3, 10, 5e-4, 10000, 3000, 100, 1e-2,
                                           100, 1.3e-5, 0, 6.5e-2, 2.0e-2, 1e-2,
                                           7e-2, 0)
                                }
           
    }


def create_society(name, soc_type):

    try:
        init_values = socity_types[name][soc_type]
        return Society(*init_values)
    except KeyError:
        raise ValueError('Unknown society type: {0} {1}'.format(name, soc_type))


def plot_society(time, commoner_population, elite_population, nature, wealth):
    plt.clf()
    plt.subplot(411)
    plt.plot(time, commoner_population)
    plt.ylabel('Commoner population', fontdict = {'fontsize' : 'x-small'})
    plt.subplot(412)
    plt.plot(time, elite_population)
    plt.ylabel('Elite population', fontdict = {'fontsize' : 'x-small'})
    plt.subplot(413)
    plt.plot(time, nature)
    plt.ylabel('Nature (eco-$)', fontdict = {'fontsize' : 'x-small'})
    plt.subplot(414)
    plt.plot(time, wealth)
    plt.ylabel('Wealth (eco-$)', fontdict = {'fontsize' : 'x-small'})
    plt.xlabel('Time (years)')
    plt.show()
    
#soc = Society(5e-3, 1, 5e-4, 100, 0, 100, 1e-2, 100, 6.67e-6, 0, 3e-2, 3e-2, 1e-2, 7e-2, 0)
#soc = create_society('egalitarian', 'collapse')
soc = create_society('unequal', 'oscillatory') 
print(soc.wealth_threshold, soc.commoner_death_rate, soc.elite_death_rate, soc.commoner_death_rate, soc.elite_death_rate)
time, commoner_population, elite_population, nature, wealth = soc.evolve(1000)
plot_society(time, commoner_population, elite_population, nature, wealth)
"""plt.subplot(411)
plt.plot(time, commoner_population)
plt.subplot(412)
plt.plot(time, elite_population)
plt.subplot(413)
plt.plot(time, nature)
plt.subplot(414)
plt.plot(time, wealth)
plt.show()"""
#for i, year in enumerate(time):
#    print year, commoner_population[i], elite_population[i], nature[i], wealth[i]  
#for i in range(10):
#    print soc.next()

#y0, t0 = [1.0, 1.0, 1.0, 1.0], 0



#r = ode(state).set_integrator('dopri5')
#r.set_initial_value(y0, t0)
#t1 = 10
#dt = 1
#while r.successful() and r.t < t1:
#    r.integrate(r.t+dt)
#    print("%g %s" % (r.t, r.y))


