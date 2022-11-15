import console from "console";
import { defineStore } from "pinia"
import { useFlatpassStore } from '../stores/flatpassStore'

export const useTransferStore = defineStore("transferStore", {
    state: () => {
        return {
            transferMode: null,
            pokemonId: "",
            receivedPokemon: null,
            isPending: false,
            progress: 0,
            transferableSortBy: "name",
            transferablePokemons: [] as any[]
        };
    },
    actions: {
        setMode(mode) {
            this.transferMode = mode
        },
        setPkmnId(id: string) {
            this.pokemonId = id
        },
        setReceivedPkmn(pkmn) {
            this.receivedPokemon = pkmn
        },
        setTransferPending(isPending) {
            this.isPending = isPending
        },
        setTransferProgress(progress) {
            this.progress = progress
        },
        setTransferablePkmns(pokemons) {
            this.transferablePokemons = pokemons
        },
        setTransferablePkmn(pokemon) {
            if (!pokemon) return

            const index = this.transferablePokemons.findIndex(
                (pkmn) => pkmn.id === pokemon.id
            )
            
            this.transferablePokemons.splice(index, 1, pokemon)
        },
        setTransferableSortBy(sortBy) {
            this.transferableSortBy = sortBy
        },
        sortTransferablePokemons() {
            this.transferablePokemons.sort((px, py) => {
                if (this.transferableSortBy === 'level')
                    return px.level - py.level
                else if (this.transferableSortBy === 'index')
                    return px.index - py.index
                else
                    return px.name.localeCompare(py.name)
            })
        },
        filterTransferablePkmns() {

        },
        resetSelectedPkmn() {
            this.pokemonId = ""
            this.receivedPokemon = null
        },
        deletePkmnFromTransferableAndReset(pokemon) {
            this.transferablePokemons = this.transferablePokemons.filter(pkmn =>
                pkmn.id !== pokemon.id
            )
            this.resetSelectedPkmn()
        }
    },
    getters: {
        // tranfer infos getters
        selectedMode(): any {
            return this.transferMode
        },
        isGtsToNds(): boolean {
            return this.selectedMode?.pf === "gts-nds"
        },
        isNdsToGts(): boolean {
            return this.selectedMode?.pf === "nds-gts"
        },
        isTransferPending(): boolean {
            return this.isPending
        },
        transferProgress(): number {
            return this.progress
        },
        isTransferDisabled() {
            const fpStore = useFlatpassStore()

            return (!fpStore.isFgtsRunnig // || !fpStore.isNdsConnected)
            || !this.selectedMode
            || (!this.isValidTransferablePkmn && this.isGtsToNds) 
            || this.isTransferPending)
        },
        // pokemon getters
        selectedPkmn(): any {
            const pkm = this.transferablePkmns.find(pkmn => pkmn.id === this.pokemonId)

            return pkm ? pkm : (this.receivedPkmn ? this.receivedPkmn : {})
        },
        selectedPkmnId(): string {
            return this.pokemonId !== "" ? this.pokemonId : (this.selectedPkmn?.id ? this.selectedPkmn.id : "")
        },
        selectedPkmnHiddenPower(): string {
            const bp = this.selectedPkmn.hidden_power?.base_power
            const pt = this.selectedPkmn.hidden_power?.power_type

            return (bp && pt) ? `${bp} (${pt})` : "none"
        },
        selectedPkmnHeldItem(): string {
            return this.selectedPkmn?.holding?.toLocaleLowerCase()
        },
        isHoldingItem(): boolean {
            return this.selectedPkmnHeldItem !== "nothing"
        },
        isValidTransferablePkmn(): boolean {
            return (this.selectedPkmnId != "" && this.transferablePkmns.some(p => p.id === this.selectedPkmnId))
        },
        transferablePkmns(): any[] {
            // Allow Gen5 => Gen4 (newer to older gens) transfers,
            // only for Pokemons that belong to older gen
            if (this.selectedMode?.pf === 'gts-nds' && this.selectedMode?.gen === 4)
                /**
                 * TODO [Gen5 handling]: add origin_game field in Pokemon object
                 * The filter by Nat. Index is good to avoid errors,
                 *   when trying to transfer unavailable Pokemons for older gens (example: send Zekrom to DPPt must be impossible)
                 *   but it's bad when transfering Pokemon with newer types, attacks or abilities to older gens...
                 **/ 
                return this.transferablePokemons.filter(pkmn => pkmn.index <= 493)
            return this.transferablePokemons
        },
        receivedPkmn(): any {
            return this.receivedPokemon;
        },
        shouldDisplayTransferContent(): boolean {
            /**
             * Display transfer content (Pokemon infos) when:
             * - A "Pokemon to Transfer" is selected, when "GTS to ..." is selected
             * OR
             * - A Pokemon has been received/stored in the GTS DB
             */
            return (this.isGtsToNds && this.transferablePkmns.find(p => p.id === this.selectedPkmnId))
                || (this.isNdsToGts && this.receivedPkmn)
        },
    }
});