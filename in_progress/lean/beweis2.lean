import algebra.module.basic
import analysis.calculus.local_extr
import data.complex.exponential
import data.equiv.basic
import data.finset.basic
import data.matrix.basic
import data.nat.basic
import data.polynomial.basic
import data.polynomial.eval
import data.polynomial.monomial
import data.polynomial.ring_division
import data.real.basic
import data.set.intervals.basic
import linear_algebra.dimension
import linear_algebra.matrix
import measure_theory.lebesgue_measure
import tactic
import data.real.basic
import linear_algebra.dimension

open_locale big_operators

open real

-- Definition der Räume S^m,k(Tₙ) und der Hutfunktionen
def spline_space (m k n : ℕ) (T : fin n → ℝ) : Type :=
  Π i, i < n → C^k (Icc (T i) (T (i+1))) → P (T i) (T (i+1)) m

def hat_function (n : ℕ) (T : fin (n+1) → ℝ) (i : fin (n+1)) : ℝ → ℝ :=
  λ x, if x ∈ Icc (T i) (T (i+1)) then 1 else 0

-- Hilfslemma: Monombasis ist in S^m,k(Tₙ) enthalten
lemma monomial_basis_in_spline_space (m k n : ℕ) (T : fin n → ℝ) :
  (λ (i : fin (m - 1)), λ (x : ℝ), x^i.val) ∈ spline_space m k n T :=
begin
  intros i hi c hc,
  have hci : c i hi = 0,
  { simp only [hat_function, subtype.val_eq_coe],
    rw [←integral_zero_of_ae_eq_zero (λ x, (x ^ (i : ℕ)).val * c i hi)],
    rw [←integral_indicator (Icc (T i) (T (i+1))) (λ x, (x ^ (i : ℕ)).val * c i hi)],
    rw integral_zero,
    rw [←submodule.coe_zero, ←hc i hi],
    apply integral_congr_ae,
    refine set.indicator_congr_ae (set.indicator_ae_eq_of_le' _ _) _,
    { exact λ x hx, hx.2 },
    { exact λ x hx, hx.1 },
    { exact ae_strongly_measurable_pow (i : ℕ) (c i hi) (Icc (T i) (T (i+1))) } },
  rw hci,
  exact polynomial.zero_apply,
end

-- Beweis des Satzes 12.2
theorem dimension_of_spline_space (m k n : ℕ) (T : fin n → ℝ) :
  dimension (spline_space m k n T) = n + m :=
begin
  induction m with m' ih,
  { -- Fall m = 0
    rw zero_add,
    refl },
  { -- Fall m = m' + 1
    rw [add_comm, nat.succ_eq_add_one],
    have h₁ : dimension (spline_space m' k n T) = n + m',
    { exact ih },
    have h₂ : dimension (spline_space m' k n T) = dimension (spline_space m' k n T) + 0,
    { rw add_zero },
    rw [h₂, ←h₁],
    apply linear_independent_iff_forall_not_mem_span.mp,
    intros f hf,
    have h₃ : f ∈ submodule.span ℝ (spline_space m' k n T),
    { rw submodule.mem_span,
      intros i hi,
      by_cases hi' : i < n,
      { exact hf i hi' },
      { exact polynomial.zero } },
    by_cases hzero : ∀ i hi, f i hi = 0,
    { -- Fall: Alle Koeffizienten cᵢ = 0
      apply exists_finite_dimensional_extension_of_finite_dimensional,
      intro f',
      have h : f' ∈ spline_space (m' + 1) k n T,
      { intros i hi,
        by_cases hi' : i < n,
        { exact c i hi' },
        { exact polynomial.zero } },
      use h,
      apply exists_linear_independent_extension,
      rw linear_independent_iff_forall_not_mem_span,
      intros g hg,
      have hfg : f + g ∈ submodule.span ℝ (spline_space m' k n T),
      { rw ←hf,
        rw linear_independent_iff_forall_eq_zero.mp (dimension_eq_card_linear_independent _),
        intro i,
        exact add_eq_zero_iff_eq.mp (hg i) },
      have hfg' : f + g = f + g,
      { refl },
      rw ←hfg' at hfg,
      exact hf (submodule.add_mem _ h₃ hfg) },
    { -- Fall: mindestens ein Koeffizient cᵢ ≠ 0
      push_neg at hzero,
      obtain ⟨i, hi, hci⟩ := hzero,
      have hmono : (λ (i : fin (m' - 1)), λ (x : ℝ), x^i.val) i hi ≠ 0,
      { intro h,
        exact hci (function.funext_iff.mp h) },
      have hmono' : (λ (i : fin (m' - 1)), λ (x : ℝ), x^i.val) ∈ spline_space m' k n T,
      { apply monomial_basis_in_spline_space },
      have hadd : (λ (i : fin (m' - 1)), λ (x : ℝ), x^i.val) + f ∈ submodule.span ℝ (spline_space m' k n T),
      { rw ←hf,
        rw linear_independent_iff_forall_eq_zero.mp (dimension_eq_card_linear_independent _),
        intro i',
        by_cases hii' : i = i',
        { rw hii',
          exact add_eq_zero_iff_eq.mp (hci.symm.trans (submodule.zero_mem _)) },
        { exact add_eq_zero_iff_eq.mp (hf i') } },
      have hadd' : (λ (i : fin (m' - 1)), λ (x : ℝ), x^i.val) + f = f,
      { refl },
      rw ←hadd' at hadd,
      exact hf (submodule.add_mem _ h₃ hadd) } }
end
