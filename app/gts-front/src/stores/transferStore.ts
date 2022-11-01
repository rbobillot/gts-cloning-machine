import { defineStore } from "pinia";

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
        setPkmnId(id) {
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
    },
    getters: {
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
        selectedPkmnId(): string {
            return this.pokemonId
        },
        transferablePkmns(): any[] {
            return this.transferablePokemons
        },
        selectedPkmn(): any {
            const pkm = this.transferablePkmns.find(pkmn => pkmn.id === this.selectedPkmnId)

            return pkm ? pkm : {}
        },
        receivedPkmn(): any {
            return this.receivedPokemon;
        }
    }
});