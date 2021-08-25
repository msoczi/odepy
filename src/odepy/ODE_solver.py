##########################
####### ODE_SOLVER #######
##########################


class ODE_solver:
    """
    A class used to represent an Animal

    ...

    Attributes
    ----------
    equation : function
        function defining the equation to be solved
    N : int
        is an integer specifying the number of points at which the equation is calculated.
        Generally, the greater the number, the more accurate the solution.
    T : float
        the upper boundary of the interval [t_0, T] on which we solve the equation
    t0 : float
        the lower boundary of the interval [t_0, T] on which we solve the equation
    *args : float
        a set of initial conditions for dependent variables in the order x_0, x_1, x_2, ... .
        Depending on the order of the equation, an appropriate number of initial conditions should be given.
        For example, for an equation of order 2, two numbers should be given x_0(t_0), x_1(t_0)
    
    Methods
    -------
    euler()
        Use Euler schema to solve equation.
    rk2()
        Use 2th Order Runge-Kutta scheme to solve equation.
    rk4()
        Use 4th Order Runge-Kutta scheme to solve equation.
    heun()
        Use Heun schema to solve equation.
    """
    
    def __init__(self, equation, N, T, t0, *args):
        self.equation = equation
        self.T = T # górne ograniczenie czasu
        self.N = N # liczba punktów do ewaluacji
        self.eq_order = len(args) # rząd równania
        self.t_values = [t0] # lista czasów z elementem t0 - czasem początkowym
        for idx, item in enumerate(args): # lista z elementami kolejnych zmiennych zależnych x_0,x_1,...,x_n
            setattr(self, "x{}_values".format(idx), [item])

    def solve(self, method = 'rk4'):

        def euler():
            h=(self.T-self.t_values[0])/self.N # Integration step
            t = self.t_values[0] # iniscjalizacja czasu
            indep_vars = [getattr(self, name) for name in ['x'+str(i)+'_values' for i in range(self.eq_order)]]
            indep_vars = [i[0] for i in indep_vars]  # aktualne wartości kolejnych zmiennych x0,x_1,...,xn

            for k in range(1, self.N+1): # pętla do ewaluacji w każdym z N punktów
                for i in range(self.eq_order): # pętla do uaktualnienia wartości zmiennych zależnych
                    indep_vars[i]=indep_vars[i]+h*self.equation(t, *indep_vars)[i]
                    getattr(self, 'x'+str(i)+'_values').append(indep_vars[i])

                t=self.t_values[0]+k*h # aktualizacja czasu
                self.t_values.append(t)

        def rk2():
            h=(self.T-self.t_values[0])/self.N # Integration step
            t = self.t_values[0] # iniscjalizacja czasu
            indep_vars = [getattr(self, name) for name in ['x'+str(i)+'_values' for i in range(self.eq_order)]]
            indep_vars = [i[0] for i in indep_vars]  # aktualne wartości kolejnych zmiennych x0,x_1,...,xn

            # Slopes at the initial points
            k1=self.equation(t, *indep_vars)
            k2=self.equation(t+0.5*h, *[a+b*0.5*h for a,b in zip(indep_vars, k1)])

            for k in range(1, self.N+1): # pętla do ewaluacji w każdym z N punktów
                for i in range(self.eq_order): # pętla do uaktualnienia wartości zmiennych zależnych
                    indep_vars[i]=indep_vars[i]+h*k2[i]
                    getattr(self, 'x'+str(i)+'_values').append(indep_vars[i])

                t=self.t_values[0]+k*h # aktualizacja czasu
                self.t_values.append(t)
                # Slopes at the following points
                k1=self.equation(t, *indep_vars)
                k2=self.equation(t+0.5*h, *[a+b*0.5*h for a,b in zip(indep_vars, k1)])

        def rk4():
            h=(self.T-self.t_values[0])/self.N # Integration step
            t = self.t_values[0] # iniscjalizacja czasu
            indep_vars = [getattr(self, name) for name in ['x'+str(i)+'_values' for i in range(self.eq_order)]]
            indep_vars = [i[0] for i in indep_vars]  # aktualne wartości kolejnych zmiennych x0,x_1,...,xn

            # Slopes at the initial points
            k1=self.equation(t, *indep_vars)
            k2=self.equation(t+(1/2)*h, *[a+b*(1/2)*h for a,b in zip(indep_vars, k1)])
            k3=self.equation(t+(1/2)*h, *[a+b*(1/2)*h for a,b in zip(indep_vars, k2)])
            k4=self.equation(t+h, *[a+b*h for a,b in zip(indep_vars, k3)])

            for k in range(1, self.N+1): # pętla do ewaluacji w każdym z N punktów
                for i in range(self.eq_order): # pętla do uaktualnienia wartości zmiennych zależnych
                    indep_vars[i]=indep_vars[i]+h*((1/6)*k1[i]+(1/3)*k2[i]+(1/3)*k3[i]+(1/6)*k4[i])
                    getattr(self, 'x'+str(i)+'_values').append(indep_vars[i])

                t=self.t_values[0]+k*h # aktualizacja czasu
                self.t_values.append(t)
                # Slopes at the following points
                k1=self.equation(t, *indep_vars)
                k2=self.equation(t+(1/2)*h, *[a+b*(1/2)*h for a,b in zip(indep_vars, k1)])
                k3=self.equation(t+(1/2)*h, *[a+b*(1/2)*h for a,b in zip(indep_vars, k2)])
                k4=self.equation(t+h, *[a+b*h for a,b in zip(indep_vars, k3)])

        def heun():
            h=(self.T-self.t_values[0])/self.N # Integration step
            t = self.t_values[0] # iniscjalizacja czasu
            indep_vars = [getattr(self, name) for name in ['x'+str(i)+'_values' for i in range(self.eq_order)]]
            indep_vars = [i[0] for i in indep_vars]  # aktualne wartości kolejnych zmiennych x0,x_1,...,xn

            # Slopes at the initial points
            k1=self.equation(t, *indep_vars)
            k2=self.equation(t+(1/3)*h, *[a+b*(1/3)*h for a,b in zip(indep_vars, k1)])
            k3=self.equation(t+(2/3)*h, *[a+b*(2/3)*h for a,b in zip(indep_vars, k2)])

            for k in range(1, self.N+1): # pętla do ewaluacji w każdym z N punktów
                for i in range(self.eq_order): # pętla do uaktualnienia wartości zmiennych zależnych
                    indep_vars[i]=indep_vars[i]+h*((1/4)*k1[i]+(3/4)*k3[i])
                    getattr(self, 'x'+str(i)+'_values').append(indep_vars[i])

                t=self.t_values[0]+k*h # aktualizacja czasu
                self.t_values.append(t)
                # Slopes at the following points
                k1=self.equation(t, *indep_vars)
                k2=self.equation(t+(1/3)*h, *[a+b*(1/3)*h for a,b in zip(indep_vars, k1)])
                k3=self.equation(t+(2/3)*h, *[a+b*(2/3)*h for a,b in zip(indep_vars, k2)])

        if method == 'rk4':
            rk4()
        elif method == 'rk2':
            rk2()
        elif method == 'euler':
            euler()
        elif method == 'heun':
            heun()
        else:
            raise TypeError(f"Wrong method argument. There is not '{method}' method available.")
            
