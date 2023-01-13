using DynamicalSystems, Plots

function generateinstance(β, p₀, p₁)
    @inline @inbounds function evolution!(nextstate, state, parameters, t)
        pₜ_₁, pₜ₋₂ = state
        nextstate[1] = 1/(1 + exp(- β* pₜ_₁ *(pₜ_₁ - pₜ₋₂))) * pₜ_₁	#Next pₜ
        nextstate[2] = pₜ_₁ #Next pₜ_₁
    end
    initial_state = [p₀, p₁] # Two dimensional dynamical system!
    return DiscreteDynamicalSystem(evolution!, initial_state, parameters)
end

T = 60
p₀ = 0.1
p₁ = 0.1
ds = generateinstance(1.0, p₀, p₁)
plot(trajectory(ds, T)[:, 1],marker = (:circle, :black),label = nothing, title = "Two cycle for β = 1.8 and c₁ = 1.0", xlabel = "t", ylabel = "P_t")