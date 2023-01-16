using DynamicalSystems, Plots
using LaTeXStrings
function generateinstance(a, p₀, p₁, p₂; R = 1.01)
    @inline @inbounds function evolution!(nextstate, state, parameters, t)
        p_t1, p_t2, p_t3    = state
        β, g, b = parameters
        num1 = exp(β*(p_t1 - R*p_t2)*(g*p_t3 - R*p_t2))
        num2 = exp(β*(p_t1 - R*p_t2)*(b -R*p_t2))
        den = num1 + num2
        nextstate[1] = (num1 * g * p_t1 + num2 * b)/(den * R)	#Next pₜ
        nextstate[2] = p_t1 #Next pₜ_₁
        nextstate[3] = p_t2 #Next pₜ_2
    end
    parameters = a
    initial_state = [p₀, p₁, p₂] # Three dimensional dynamical system!
    return DiscreteDynamicalSystem(evolution!, initial_state, parameters)
end

T = 60
p₀ = 0.1
p₁ = 0.1
p₂ = 0.1
ds = generateinstance([1.0, 0.9,2.0], p₀, p₁, p₂)
evolution = plot(trajectory(ds, T)[:, 1],marker = (:circle, :black),label = nothing, title = L"Evolution", xlabel = L"t", ylabel = L"P_t")
savefig(evolution, "time_evolution.png")

function computeorbit(
    ds, alimits; 
    n = 2_000, 	# Number of points
    L = 500,
    xindex = 1, 	# Index of the state variables in the dynamical system
    aindex = 1, 	# Index of the parameter in the dynamical system
    kwargs...
)

a0, a1 = alimits
P = range(a0, a1, length = L)
orbits = orbitdiagram(
    ds, xindex, aindex, P; 
    n = n, Ttr = 2000, kwargs...
)
x = Vector{Float64}(undef, n*L) # Empty vector to store points
y = copy(x)
for j in 1:L
    x[(1 + (j-1)*n):j*n] .= P[j]
    y[(1 + (j-1)*n):j*n] .= orbits[j]
end
return x, y
end

x, y = computeorbit(ds, (10, 20.0), aindex = 1)
	
bifurcation = scatter(x, y,
	xaxis = L"g", ylabel = L"p", 
	ms = 1.5, color = :black, legend = nothing,
	alpha = 0.05
)

savefig(bifurcation, "two_types_bifurcation_g.png")
### Lyapunov Exponent

aspace = range(1.0, 1.4, length = 500)
λs = zeros(length(aspace))
	
for (i, a) in enumerate(aspace)
    set_parameter!(ds, 1, a)
    λs[i] = lyapunov(ds, 8_000; Ttr = 500)
end
	
plot(
	aspace, λs, 
	xlabel = "a", ylabel = "lambda", label = nothing,
	title = "Lyapunov exponent")

savefig(plot(
	aspace, λs, 
	xlabel = "a", ylabel = "lambda", label = nothing,
	title = "Lyapunov exponent"), "Lyapunov_exponent.png")